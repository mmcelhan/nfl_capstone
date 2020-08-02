
var USER_SPEED = "fast";

var width = 750,
    height = 750,
	padding = 1,
	maxRadius = 3;
	// color = d3.scale.category10();

var sched_objs = [],
	curr_minute = 0;

var act_codes = [
	{"index": "0", "short": "Quarterback", "desc": "QB"},
	{"index": "1", "short": "Wide Receiver", "desc": "WR"},
	{"index": "2", "short": "Runningback", "desc": "RB"},
	{"index": "3", "short": "Other", "desc": "Other"},
	{"index": "4", "short": "Cornerback", "desc": "CB"},
	{"index": "5", "short": "No pick", "desc": "No pick"},
];


var speeds = { "slow": 200, "medium": 125, "fast": 60 };


var time_notes = [
	{ "start_minute": 1, "stop_minute": 51, "year": "2000", "img": "img/2000.png", "color": "white", "note": "In 2000 Courtney Brown from Penn State is the #1 Pick by the Browns to play as a Defensive End." },
	{ "start_minute": 54, "stop_minute": 104, "year": "2001", "img": "img/2001.png",  "color": "white", "note": "In 2001 Michael Vick from Virginia Tech is the #1 Pick by the Falcons to play as a Quarterback." },
	{ "start_minute": 107, "stop_minute": 157, "year": "2002", "img": "img/2002.png",  "color": "white", "note": "In 2002 David Carr from Fresno State is the #1 Pick by the Texans to play as a Quarterback." },
	{ "start_minute": 160, "stop_minute": 210, "year": "2003", "img": "img/2003.png",  "color": "white", "note": "In 2003 Carson Palmer from USC is the #1 Pick by the Bengals to play as a Quarterback." },
	{ "start_minute": 213, "stop_minute": 263, "year": "2004", "img": "img/2004.png",  "color": "white", "note": "In 2004 Eli Manning from Mississippi is the #1 Pick by the Chargers to play as a Quarterback." },
	{ "start_minute": 266, "stop_minute": 316, "year": "2005", "img": "img/2005.png",  "color": "white", "note": "In 2005 Alex Smith from Utah is the #1 Pick by the 49ers to play as a Quarterback." },
	{ "start_minute": 319, "stop_minute": 369, "year": "2006", "img": "img/2006.png",  "color": "white", "note": "In 2006 Mario Williams from North Carolina State is the #1 Pick by the Texans to play as a Defensive End." },
	{ "start_minute": 372, "stop_minute": 422, "year": "2007", "img": "img/2007.png",  "color": "white", "note": "In 2007 JaMarcus Russell from Louisiana State is the #1 Pick by the Raiders to play as a Quarterback." },
	{ "start_minute": 425, "stop_minute": 475, "year": "2008", "img": "img/2008.png",  "color": "white", "note": "In 2008 Jake Long from Michigan is the #1 Pick by the Dolphins to play as a Offensive Tackle." },
	{ "start_minute": 478, "stop_minute": 524, "year": "2009", "img": "img/2009.png",  "color": "white", "note": "In 2009 Matthew Stafford from Georgia is the #1 Pick by the Lions to play as a Quarterback." },
	{ "start_minute": 531, "stop_minute": 577, "year": "2010", "img": "img/2010.png",  "color": "white", "note": "In 2010 Sam Bradford from Oklahoma is the #1 Pick by the Rams to play as a Quarterback." },
    { "start_minute": 584, "stop_minute": 630, "year": "2011", "img": "img/2011.png",  "color": "white", "note": "In 2011 Cam Newton from Auburn is the #1 Pick by the Panthers to play as a Quarterback." }, 
    { "start_minute": 637, "stop_minute": 683, "year": "2012", "img": "img/2012.png",  "color": "white", "note": "In 2012 Andrew Luck from Stanford is the #1 Pick by the Colts to play as a Quarterback." },
    { "start_minute": 690, "stop_minute": 740, "year": "2013","img": "img/2013.png",  "color": "white", "note": "In 2013 Eric Fisher from Central Michigan is the #1 Pick by the Chiefs to play as a Offensive Tackle." },
    { "start_minute": 743, "stop_minute": 789, "year": "2014", "img": "img/2014.png",  "color": "white", "note": "In 2014 Jadeveon Clowney from South Carolina is the #1 Pick by the Texans to play as a Defensive End." },
    { "start_minute": 796, "stop_minute": 840, "year": "2015", "img": "img/2015.png",  "color": "white", "note": "In 2015 Jameis Winston from Florida State is the #1 Pick by the Buccaneers to play as a Quarterback." },
    { "start_minute": 849, "stop_minute": 895, "year": "2016", "img": "img/2016.png",  "color": "white", "note": "In 2016 Jared Goff from California is the #1 Pick by the Rams to play as a Quarterback." },
    { "start_minute": 902, "stop_minute": 952, "year": "2017", "img": "img/2017.png",  "color": "white", "note": "In 2017 Myles Garrett from Texas A&M is the #1 Pick by the Browns to play as a Defensive End." },    
    { "start_minute": 955, "stop_minute": 1001, "year": "2018", "img": "img/2018.png",  "color": "white", "note": "In 2018 Baker Mayfield from Oklahoma is the #1 Pick by the Browns to play as a Quarterback." },
    { "start_minute": 1008, "stop_minute": 1058, "year": "2019", "img": "img/2019.png",  "color": "white", "note": "In 2019 Kyler Murray from Oklahoma is the #1 Pick by the Cardinals to play as a Quarterback." }, 
    { "start_minute": 1061, "stop_minute": 1111, "year": "2020", "img": "img/2020.png",  "color": "white", "note": "In 2020 Joe Burrow from Louisiana State is the #1 Pick by the Bengals to play as a Quarterback." }, 

];
var notes_index = 0;


// Activity to put in center of circle arrangement
var center_act = "No pick",
	center_pt = { "x": 380, "y": 365 };


// Coordinates for activities
var foci = {};
act_codes.forEach(function(code, i) {
	if (code.desc == center_act) {
		foci[code.index] = center_pt;
	} else {
		var theta = 2 * Math.PI / (act_codes.length-1);
		foci[code.index] = {x: 250 * Math.cos((i - 1) * theta)+380, y: 250 * Math.sin((i - 1) * theta)+365 };
	}
});


// Start the SVG
var svg = d3.select("#chart").append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr('position', 'absolute')
    .attr('left', '200px')
    .attr('top', '200px');


// Load data and let's do it.
d3.tsv("data/schema.tsv", function(error, data) {

	data.forEach(function(d) {
		var day_array = d.day.split(",");
		var activities = [];
		for (var i=0; i < day_array.length; i++) {
			// Duration
			if (i % 2 == 1) {
				activities.push({'act': day_array[i-1], 'duration': +day_array[i]});
			}
		}
		sched_objs.push(activities);
	});

	// Used for percentages by minute
	var act_counts = { "0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0 };

	// A node for each person's schedule
	var nodes = sched_objs.map(function(o,i) {
		var act = o[0].act;
		act_counts[act] += 1;
		var init_x = foci[act].x + Math.random();
		var init_y = foci[act].y + Math.random();
		return {
			act: act,
			radius: 3,
			x: init_x,
			y: init_y,
			color: color(act),
			moves: 0,
			next_move_time: o[0].duration,
			sched: o,
		}
	});

	var force = d3.layout.force()
		.nodes(nodes)
		.size([width, height])
		// .links([])
		.gravity(0)
		.charge(0)
		.friction(.9)
		.on("tick", tick)
		.start();

	var circle = svg.selectAll("circle")
		.data(nodes)
	    .enter().append("circle")
		.attr("r", function(d) { return d.radius; })
		.style("fill", function(d) { return d.color; });
		// .call(force.drag);

	// Activity labels
	var label = svg.selectAll("text")
		.data(act_codes)
	  .enter().append("text")
		.attr("class", "actlabel")
		.attr("x", function(d, i) {
			if (d.desc == center_act) {
				return center_pt.x;
			} else {
				var theta = 2 * Math.PI / (act_codes.length-1);
				return 340 * Math.cos((i - 1) * theta)+380;
			}

		})
		.attr("y", function(d, i) {
			if (d.desc == center_act) {
				return center_pt.y;
			} else {
				var theta = 2 * Math.PI / (act_codes.length-1);
				return 340 * Math.sin((i - 1) * theta)+365;
			}

		});

	label.append("tspan")
		.attr("x", function() { return d3.select(this.parentNode).attr("x"); })
		// .attr("dy", "1.3em")
		.attr("text-anchor", "middle")
		.text(function(d) {
			return d.short;
		});
	label.append("tspan")
		.attr("dy", "1.3em")
		.attr("x", function() { return d3.select(this.parentNode).attr("x"); })
		.attr("text-anchor", "middle")
		.attr("class", "actpct")
		.text(function(d) {
			return act_counts[d.index] + "%";
		});


	// Update nodes based on activity and duration
	function timer() {
		d3.range(nodes.length).map(function(i) {
			var curr_node = nodes[i],
				curr_moves = curr_node.moves;

			// Time to go to next activity
			if (curr_node.next_move_time == curr_minute) {
				if (curr_node.moves == curr_node.sched.length-1) {
					curr_moves = 0;
				} else {
					curr_moves += 1;
				}

				// Subtract from current activity count
				act_counts[curr_node.act] -= 1;

				// Move on to next activity
				curr_node.act = curr_node.sched[ curr_moves ].act;

				// Add to new activity count
				act_counts[curr_node.act] += 1;

				curr_node.moves = curr_moves;
				curr_node.cx = foci[curr_node.act].x;
				curr_node.cy = foci[curr_node.act].y;

				nodes[i].next_move_time += nodes[i].sched[ curr_node.moves ].duration;
			}

		});

		force.resume();
		curr_minute += 1;

		// Update percentages
		label.selectAll("tspan.actpct")
			.text(function(d) {
				return readablePercent(act_counts[d.index]);
			});

		// Update year and notes
		var true_minute = curr_minute % 1440;
		if (true_minute == time_notes[notes_index].start_minute) {
		    d3.select("#year")
		        .style("color", "#fffced")
		        .style("text-align", "left")
		        .style("font-size", "300%")
				.style("font-family", "adobe-caslon-pro")
				.text(time_notes[notes_index].year)
				.transition()
				.duration(500)
				.style("text-align", "center")
				.style("color", "#000000");
		}

        if (true_minute == time_notes[notes_index].start_minute + 10) {
			d3.select("#image").append('img')
			    .attr('src', time_notes[notes_index].img)
                .attr('width', 200)
                .attr('height', 250)
                .style('position', 'absolute')
                .style('top', '100px')
                .style('left', '150px')
                .style('opacity', 0)
                .style("display", "block")
                .style("background", time_notes[notes_index].color)
                .style("padding", "8px")
                .style("border", "1px solid #ccc")
                .style("box-shadow", "5px 5px 5px #999")
                .transition()
                .duration(1000)
                .style('opacity', 1);
	    }

		if (true_minute == time_notes[notes_index].start_minute + 10) {
			d3.select("#note")
				.style("top", "500px")
				.style("color", "#fffced")
				.style("font-size", "150%")
				.style("font-style", "italic")
			    .transition()
				.duration(500)
				.style("top", "370px")
				.style("color", "#000000")
				.text(time_notes[notes_index].note);
	    }

	    if (true_minute == time_notes[notes_index].stop_minute - 5) {
	        d3.select('#image')
	            .transition()
	            .duration(500)
	            .attr('opacity', 0);
	    }

		// Make note disappear at the end.
		else if (true_minute == time_notes[notes_index].stop_minute) {

			d3.select("#note").transition()
				.duration(500)
				.style("top", "500px")
				.style("color", "#fffced");

			d3.select("#year").transition()
				.duration(500)
				.style("top", "300px")
				.style("color", "#fffced");

			notes_index += 1;
			if (notes_index == time_notes.length) {
				notes_index = 0;
			}
		}


		setTimeout(timer, speeds[USER_SPEED]);
	}
	setTimeout(timer, speeds[USER_SPEED]);


	function tick(e) {
	  var k = 0.04 * e.alpha;

	  // Push nodes toward their designated focus.
	  nodes.forEach(function(o, i) {
		var curr_act = o.act;
        var damper = 1;
		o.color = color(curr_act);
	    o.y += (foci[curr_act].y - o.y) * k * damper;
	    o.x += (foci[curr_act].x - o.x) * k * damper;
	  });

	  circle
	  	  .each(collide(.5))
	  	  .style("fill", function(d) { return d.color; })
	      .attr("cx", function(d) { return d.x; })
	      .attr("cy", function(d) { return d.y; });
	}


	// Resolve collisions between nodes.
	function collide(alpha) {
	  var quadtree = d3.geom.quadtree(nodes);
	  return function(d) {
	    var r = d.radius + maxRadius + padding,
	        nx1 = d.x - r,
	        nx2 = d.x + r,
	        ny1 = d.y - r,
	        ny2 = d.y + r;
	    quadtree.visit(function(quad, x1, y1, x2, y2) {
	      if (quad.point && (quad.point !== d)) {
	        var x = d.x - quad.point.x,
	            y = d.y - quad.point.y,
	            l = Math.sqrt(x * x + y * y),
	            r = d.radius + quad.point.radius + (d.act !== quad.point.act) * padding;
	        if (l < r) {
	          l = (l - r) / l * alpha;
	          d.x -= x *= l;
	          d.y -= y *= l;
	          quad.point.x += x;
	          quad.point.y += y;
	        }
	      }
	      return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
	    });
	  };
	}




	// Speed toggle
	d3.selectAll(".togglebutton")
      .on("click", function() {
        if (d3.select(this).attr("data-val") == "slow") {
            d3.select(".slow").classed("current", true);
			d3.select(".medium").classed("current", false);
            d3.select(".fast").classed("current", false);
        } else if (d3.select(this).attr("data-val") == "medium") {
            d3.select(".slow").classed("current", false);
			d3.select(".medium").classed("current", true);
            d3.select(".fast").classed("current", false);
        }
		else {
            d3.select(".slow").classed("current", false);
			d3.select(".medium").classed("current", false);
			d3.select(".fast").classed("current", true);
        }

		USER_SPEED = d3.select(this).attr("data-val");
    });
}); // @end d3.tsv



function color(activity) {

	var colorByActivity = {
		"0": "blue",
		"1": "red",
		"2": "yellow",
		"3": "brown",
		"4": "black",
		"5": "grey",
	}

	return colorByActivity[activity];

}



// Output readable percent based on count.
function readablePercent(n) {

	var pct = 100 * n / 1000;
	if (pct < 1 && pct > 0) {
		pct = "<1%";
	} else {
		pct = Math.round(pct) + "%";
	}

	return pct;
}

