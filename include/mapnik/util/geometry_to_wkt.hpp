/*****************************************************************************
 *
 * This file is part of Mapnik (c++ mapping toolkit)
 *
 * Copyright (C) 2021 Artem Pavlenko
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

#ifndef MAPNIK_GEOMETRY_TO_WKT_HPP
#define MAPNIK_GEOMETRY_TO_WKT_HPP

// mapnik
#include <mapnik/wkt/wkt_factory.hpp>
#include <mapnik/wkt/wkt_generator_grammar.hpp>

// boost
#include <boost/spirit/include/karma.hpp>

namespace mapnik { namespace util {

inline bool to_wkt(std::string & wkt,  mapnik::geometry::geometry<double> const& geom)
{
    using sink_type = std::back_insert_iterator<std::string>;
    static const mapnik::wkt::wkt_generator_grammar<sink_type, mapnik::geometry::geometry<double>> generator;
    sink_type sink(wkt);
    return boost::spirit::karma::generate(sink, generator, geom);
}

inline bool to_wkt(std::string & wkt,  mapnik::geometry::geometry<std::int64_t> const& geom)
{
    using sink_type = std::back_insert_iterator<std::string>;
    static const mapnik::wkt::wkt_generator_grammar<sink_type, mapnik::geometry::geometry<std::int64_t>> generator;
    sink_type sink(wkt);
    return boost::spirit::karma::generate(sink, generator, geom);
}

}}



#endif // MAPNIK_GEOMETRY_TO_WKT_HPP
