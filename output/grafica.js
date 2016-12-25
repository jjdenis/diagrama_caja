
        var descriptor = {"outliers": [5, 105],
           "last_non_outlier": 2998.0,
           "media": 2258.653333333333,
           "median": 2337.0,
           "quartile_1": 1988.0,
           "quartile_3": 2650.0,
           "upper_regular_range": 3643.0,
           "maximo": 2998.0,
           "length": 75,
           "values": [5, 105, 1938.0, 1990.0, 2081.0, 2182.0, 2165.0, 2217.0, 2414.0, 2584.0, 2899.0, 2716.0, 1704.0, 2707.0, 1686.0, 2902.0, 2258.0, 2213.0, 2629.0, 1907.0, 2378.0, 2102.0, 2205.0, 2860.0, 2998.0, 2583.0, 2374.0, 1554.0, 2432.0, 1924.0, 1701.0, 2706.0, 2538.0, 2586.0, 1805.0, 2479.0, 2819.0, 1785.0, 2548.0, 2496.0, 1634.0, 1643.0, 2067.0, 2941.0, 2825.0, 2186.0, 2740.0, 2267.0, 2081.0, 2599.0, 2359.0, 2337.0, 2659.0, 1988.0, 2839.0, 2142.0, 2896.0, 2849.0, 2802.0, 1620.0, 2978.0, 2209.0, 2650.0, 2327.0, 2170.0, 1666.0, 1827.0, 2503.0, 2381.0, 2469.0, 2480.0, 2090.0, 1566.0, 2759.0, 1675.0],
           "first_non_outlier": 1554.0,
           "lower_regular_range": 995.0,
           "ultimo": 1675.0};


		var config = {	"grid_color": "rgb(82,82,82)",
						"interquartile_zone": true,
						"limite_color": "rgb(49,163,84)",
						"value_color": "rgb(0,0,0)",
						"xmin": 10,
						"width": 520,
						"height":70.0,
						"not_outlier_zone_color": "rgb(240,240,240)",
						"description_point": "",
						"not_outlier_zone": true,
						"grid_space": 500,
						"alto_barra": 20.0,
						"titulo": "",
						"outliers": true,
						"limsup": null,
						"outliers_color":
						"rgb(240,240,240)",
						"explanation": "",
						"interquartile_zone_color": "rgb(217,217,217)",
						"grid": true,
						"vmax": 4000.0,
						"liminf": null,
						"vmin": 0.0,
						"unidades": "",
						"xmax": 500,
						"y": 30.0};

			var scale = d3.scale.linear()
                    .domain([0, config.vmax])
                    .range([config.xmin, config.xmax]);

			//Create SVG element
			var svg = d3.select("body")
						.append("svg")
						.attr("width", config.width)
						.attr("height", config.height);

			svg.append("rect")
			   .attr("x", scale(descriptor.quartile_1))
			   .attr("y", config.y)
			   .attr("width", scale(descriptor.quartile_3-descriptor.quartile_1))
			   .attr("height", config.alto_barra)
			   .attr("fill", "black");
