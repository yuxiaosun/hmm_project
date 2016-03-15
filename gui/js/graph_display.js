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
function render_graph(graph, layout_width, layout_height){
  var width = layout_width | 400;
  var height = layout_height | 400;
  var nodes = graph.nodes;
  var links = graph.links;

  var svg = d3.select('body').append('svg')
      .attr('width', width)
      .attr('height', height);

  var force = d3.layout.force()
      .size([width, height])
      .nodes(nodes)
      .links(links);

  force.linkDistance(60)
    .charge(-100)
    .start();

  var loading = svg.append("text")
    .attr("x", width / 2)
    .attr("y", height / 2)
    .attr("dy", ".35em")
    .style("text-anchor", "middle")
    .text("Rendering ...");

  var link = svg.selectAll('.link')
    .data(links)
    .enter().append('line')
    .attr('class', 'link');

  var node = svg.selectAll('.node')
    .data(nodes)
    .enter().append('g')
    .attr('class', 'node');

  force.on('end', function() {

    node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

    node.append('circle')
      .attr('r', 10);
    node.append('text')
      .attr('dy', '.3em')
      .attr('text-anchor', "middle")
      .text(function(d) { return d.label; });

    link.attr('x1', function(d) { return d.source.x; })
      .attr('y1', function(d) { return d.source.y; })
      .attr('x2', function(d) { return d.target.x; })
      .attr('y2', function(d) { return d.target.y; });

    loading.remove();
  });
}

// render_graph(graph)
render_graph_file('/gui/graph.json')
