/*****************************************************************************
 *
 * This file is part of Mapnik (c++ mapping toolkit)
 *
 * Copyright (C) 2011 Artem Pavlenko
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

#ifndef MAPNIK_PARAMS_HPP
#define MAPNIK_PARAMS_HPP

// mapnik
#include <mapnik/config.hpp>
#include <mapnik/value_types.hpp>

// boost
#include <boost/variant/variant.hpp>
#include <boost/optional.hpp>

// stl
#include <string>
#include <map>

namespace mapnik
{

// fwd declare
class boolean;

typedef boost::variant<value_null,value_integer,value_double,std::string> value_holder;
typedef std::pair<std::string, value_holder> parameter;
typedef std::map<std::string, value_holder> param_map;

class MAPNIK_DECL parameters : public param_map
{
public:
    parameters() {}
    template <typename T>
    boost::optional<T> get(std::string const& key) const;
    template <typename T>
    boost::optional<T> get(std::string const& key, T const& default_opt_value) const;

};

#ifdef _MSC_VER
template MAPNIK_DECL
boost::optional<std::string> parameters::get(std::string const& key) const;
template MAPNIK_DECL
boost::optional<std::string> parameters::get(std::string const& key,
                                 std::string const& default_opt_value) const;
template MAPNIK_DECL
boost::optional<value_double> parameters::get(std::string const& key) const;
template MAPNIK_DECL
boost::optional<value_double> parameters::get(std::string const& key,
                                  value_double const& default_opt_value) const;

template MAPNIK_DECL
boost::optional<int> parameters::get(std::string const& key) const;
template MAPNIK_DECL
boost::optional<int> parameters::get(std::string const& key,
                         int const& default_opt_value) const;
#ifdef BIGINT
template MAPNIK_DECL
boost::optional<value_integer> parameters::get(std::string const& key) const;
template MAPNIK_DECL
boost::optional<value_integer> parameters::get(std::string const& key,
                                   value_integer const& default_opt_value) const;
#endif

template MAPNIK_DECL
boost::optional<mapnik::boolean> parameters::get(std::string const& key) const;
template MAPNIK_DECL
boost::optional<mapnik::boolean> parameters::get(std::string const& key,
                                     mapnik::boolean const& default_opt_value) const;

#endif

}

#endif // MAPNIK_PARAMS_HPP
