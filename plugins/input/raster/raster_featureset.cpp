/*****************************************************************************
 * 
 * This file is part of Mapnik (c++ mapping toolkit)
 *
 * Copyright (C) 2006 Artem Pavlenko
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 *
 *****************************************************************************/

// mapnik
#include <mapnik/image_reader.hpp>
#include <mapnik/image_util.hpp>
#include <mapnik/feature_factory.hpp>

#include "raster_featureset.hpp"


using mapnik::query;
using mapnik::CoordTransform;
using mapnik::image_reader;
using mapnik::Feature;
using mapnik::feature_ptr;
using mapnik::image_data_32;
using mapnik::raster;
using mapnik::feature_factory;

template <typename LookupPolicy>
raster_featureset<LookupPolicy>::raster_featureset(LookupPolicy const& policy,
                                                   box2d<double> const& extent,
                                                   query const& q)
   : policy_(policy),
     feature_id_(1),
     extent_(extent),
     bbox_(q.get_bbox()),
     curIter_(policy_.begin()),
     endIter_(policy_.end()) 
{}

template <typename LookupPolicy>
raster_featureset<LookupPolicy>::~raster_featureset() {}

template <typename LookupPolicy>
feature_ptr raster_featureset<LookupPolicy>::next()
{
   if (curIter_!=endIter_)
   {
      feature_ptr feature(feature_factory::create(feature_id_));
      ++feature_id_;
      try
      {         
         std::auto_ptr<image_reader> reader(mapnik::get_image_reader(curIter_->file(),curIter_->format()));

#ifdef MAPNIK_DEBUG         
         std::clog << "Raster Plugin: READER = " << curIter_->format() << " " << curIter_->file() 
                   << " size(" << curIter_->width() << "," << curIter_->height() << ")" << std::endl;
#endif
         if (reader.get())
         {
            int image_width=reader->width();
            int image_height=reader->height();
            
            if (image_width>0 && image_height>0)
            {
               CoordTransform t(image_width,image_height,extent_,0,0);
               box2d<double> intersect=bbox_.intersect(curIter_->envelope());
               box2d<double> ext=t.forward(intersect);
               if ( ext.width()>0.5 && ext.height()>0.5 )
               {
                  //select minimum raster containing whole ext
                  int x_off = static_cast<int>(floor(ext.minx()));
                  int y_off = static_cast<int>(floor(ext.miny()));
                  int end_x = static_cast<int>(ceil(ext.maxx()));
                  int end_y = static_cast<int>(ceil(ext.maxy()));
                  //clip to available data
                  if (x_off < 0)
                     x_off = 0;
                  if (y_off < 0)
                     y_off = 0;
                  if (end_x > image_width)
                     end_x = image_width;
                  if (end_y > image_height)
                     end_y = image_height;
                  int width = end_x - x_off;
                  int height = end_y - y_off;
                  //calculate actual box2d of returned raster
                  box2d<double> feature_raster_extent(x_off, y_off, x_off+width, y_off+height); 
                  intersect = t.backward(feature_raster_extent);

                  image_data_32 image(width,height);
                  reader->read(x_off,y_off,image);
                  feature->set_raster(boost::make_shared<raster>(intersect,image));
               }
            }
         }
      }
      catch (mapnik::image_reader_exception const& ex)
      {
          std::cerr << "Raster Plugin: image reader exception caught:" << ex.what() << std::endl;
      }
      catch (...)
      {
         std::cerr << "Raster Plugin: exception caught" << std::endl;
      }
      
      ++curIter_;
      return feature;
   }
   return feature_ptr();
}

template class raster_featureset<single_file_policy>;
template class raster_featureset<tiled_file_policy>;
