
var _charts = [ 'repartition', 'size', 'files', 'backups' ];
var _charts_obj = [];
var initialized = false;

var _clients = function() {
	var limit, aggreg;
	if (!initialized) {
		limit = 8;
		aggreg = 'number';
		$.each(_charts, function(i, j) {
			tmp =  nv.models.pieChart()
				.x(function(d) { return d.label })
				.y(function(d) { return d.value })
				.showLabels(true)
				.labelThreshold(.05)
				.labelType("percent")
				.valueFormat(d3.format('f'))
				.color(d3.scale.category20c().range())
				.labelThreshold(.05)
				.donutRatio(0.55)
				.donut(true)
				;

			tmp.tooltip.contentGenerator(function(obj) { return '<h3>'+obj.data.label+'</h3><p>'+(j == 'size' ? _bytes_human_readable(obj.data.value, false) : obj.data.value)+'</p>'; });

			_charts_obj.push({ 'key': 'chart_'+j, 'obj': tmp, 'data': [] });
		});
	} else {
		limit = $('#limit').val();
		aggreg = $('#aggreg').val();
	}
	{% if config.WITH_CELERY -%}
	url = '{{ url_for("api.async_clients_report", server=server) }}';
	{% else -%}
	url = '{{ url_for("api.clients_report", server=server) }}';
	{% endif -%}
	$.getJSON(url, {limit: limit, aggregation: aggreg}, function(d) {
		rep = [];
		size = [];
		files = [];
		backups = {};
		repartition = {};
		windows = 0;
		nonwin = 0;
		unknown = 0;
		$('.mycharts').each(function() {
			$(this).parent().show();
		});
		$.each(d['clients'], function(k, c) {
			if (c.stats.os in repartition) {
				repartition[c.stats.os]++;
			} else {
				repartition[c.stats.os] = 1;
			}
			size.push({'label': c.name, 'value': c.stats.totsize});
			files.push({'label': c.name, 'value': c.stats.total});
		});
		$.each(d['backups'], function(k, c) {
			backups[c.name] = c.number;
		});
		rep = [];
		$.each(repartition, function(label, value) {
			rep.push({'label': label, 'value': value});
		});
		$.each(_charts_obj, function(i, c) {
			switch (c.key) {
				case 'chart_repartition':
					c.data = rep;
					break;
				case 'chart_size':
					c.data = size;
					break;
				case 'chart_files':
					c.data = files;
					break;
				case 'chart_backups':
					data = [];
					$.each(backups, function(cl, num) {
						data.push({'label': cl, 'value': num});
					});
					c.data = data;
					break;
			}
		});
		_redraw();
	})
	.fail(buiFail)
	.fail(function () {
		$('.mycharts').each(function() {
			$(this).parent().hide();
		});
	});
};

var _redraw = function() {
	$.each(_charts_obj, function(i, j) {
		nv.addGraph(function() {

			d3.select('#'+j.key+' svg')
				.datum(j.data)
				.transition().duration(500)
				.call(j.obj);

			nv.utils.windowResize(j.obj.update);

			return j.obj;
		});
	});
	initialized = true;
};
