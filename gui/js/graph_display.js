function render_graph_file(filename, layout_width, layout_height){
  d3.json(filename, function(err, graph){
    if(err){
      console.log('unable to read file ', filename)
      console.log(err)
      return;
    }
    render_graph(graph, layout_width, layout_height);
  })
}

function construct_node(node, params){
  node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
  node.append('circle')
    .attr('r', params.node_radius);
  node.append('text')
    .attr('dy', '.3em')
    .attr('text-anchor', "middle")
    .text(function(d) { return d.label; });
}

function construct_link(link, params){

  // to curve edges, add arrow at middle
  link.attr("d", function(d) {
    var dx = d.target.x - d.source.x,
        dy = d.target.y - d.source.y,
        dr = Math.sqrt(dx * dx + dy * dy)/4+30,
        mx = d.source.x + dx,
        my = d.source.y + dy;
    return [
      "M",d.source.x,d.source.y,
      "A",dr,dr,0,0,1,mx,my
    ].join(" ");
  });
}

function required_radius(label_length){
  // find circle radius to fit label
  return (label_length*4 +2)+"px";
}

function required_edge_length(label_length){
  // find preferred edge length for array
  return 4*(label_length*4 +2);
}

function render_graph(graph, layout_width, layout_height){
  var width = layout_width | 400;
  var height = layout_height | 400;
  var nodes = graph.nodes;
  var links = graph.links;

  var params = {label_max : 0};

  params.label_max = nodes.reduce(function(node1, node2){
    return Math.max(node1.label.length, node2.label.length);
  })
  params.node_radius = required_radius(params.label_max);
  params.linkDistance = required_edge_length(params.label_max);

  var svg = d3.select('body').append('svg')
      .attr('width', width)
      .attr('height', height);

  var force = d3.layout.force()
      .size([width, height])
      .nodes(nodes)
      .links(links);

  force.linkDistance(params.linkDistance)
    .charge(-100)
    .start();

  var loading = svg.append("text")
    .attr("x", width / 2)
    .attr("y", height / 2)
    .attr("dy", ".35em")
    .style("text-anchor", "middle")
    .text("Rendering ...");

  // arrow for edges
  svg.append("defs").selectAll("marker")
    .data(["arrow"])
  .enter().append("marker")
    .attr("id", function(d) { return d; })
    .attr("viewBox", "0 -5 10 10")
    .attr("refX", 15)
    .attr("refY", -1.5)
    .attr("markerWidth", 6)
    .attr("markerHeight", 6)
    .attr("orient", "auto")
  .append("path")
    .attr("d", "M0,-5L10,0L0,5");


  var link = svg.selectAll('.link')
    .data(links)
    .enter().append('path')
    .attr('class', 'link')
    .attr('marker-mid', 'url(#arrow)');

  var node = svg.selectAll('.node')
    .data(nodes)
    .enter().append('g')
    .attr('class', 'node');

  force.on('end', function() {
    construct_node(node, params);
    construct_link(link, params);
    loading.remove();
    console.log(params);
  });

}

// render_graph(graph)
render_graph_file('/gui/graph.json')
