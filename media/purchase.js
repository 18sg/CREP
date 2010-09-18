document.observe("dom:loaded", function(){
	var table = new Table(0, 2);
	table.calcValues();
	
	$("add_col").onclick = table.add_col.bind(table);
	
	// prevent the form from sending when Return key is pressed
	Event.observe('add_purchase_form', 'keydown', function(event) {
		if (event.keyCode == 13)
			event.stop();
	});
});

function evenRound(num) {
	return (Math.floor(num) % 2 == 0 && num % 1 == 0.5) 
		? Math.floor(num) 
		: Math.round(num);
}

var Table = Class.create();

Table.prototype = {
	initialize: function(width, height) {
		this.width = width;
		this.height = $$("tr.w").length;
		this.row_names = $$("tr.w").map(function(row){return row.id});
		this.table = $("table");
		this.setup_events();
	},
	
	setup_events: function() {
		$$("table input").each(function(e) {e.onkeyup = this.calcValues.bind(this);},
		                       this);
	},
	
	add_col: function() {
		var table = this;
		var make_elem = function(row, col) {
			var on_click = function() {
				$(this).setValue("1");
				this.onclick = null;
				table.calcValues();
			};
			var input = new Element("input", {id: row + "_" + col,
			                                  value: "0"});
			input.onclick = on_click;
			var td = new Element("td", {"class": "w"}).update(input);
			return td;
		};
		
		this.width++;
		$$("tr.w").each(function(row) {
			var last = $$("#" + row.id + " td.w").last();
			var new_td = new Element("td");
			last.insert({after: new_td});
			new_td.insert({after: make_elem(row.id, this.width)});
		}, this);
		
		var new_math = new Element("td").update("+");
		var new_input = new Element("td", {"class": "t"}).update(
			new Element("input", {id: "t_" + this.width, value: "0"}));
		$$("td.t").last().insert({after: new_math});
		new_math.insert({after: new_input});
		
		this.setup_events();
	},
	
	get_input: function(name) {
		return evenRound(eval($F(name)) * 100);
	},
	
	format_num: function(num) {
		return (new Number(evenRound(num) / 100)).toFixed(2)
	},
	
	calcValues: function() {
		total_price = this.get_input("t_t");
		totals = {};
		person_totals = {}
		for (x = 0; x < this.height; x++)
			person_totals[x] = 0;
		totals[0] = total_price;
		for (y = 1; y <= this.width; y++)
		{
			totals[y] = this.get_input("t_" + y);
			totals[0] -= totals[y];
		}
		$("t_0").innerText = this.format_num(totals[0]);
		
		for (y = 0; y <= this.width; y++)
		{
			total_weighting = 0.0;
			for (x = 0; x < this.height; x++)
				total_weighting += this.get_input(this.row_names[x] + "_" + y);
			if (total_weighting > 0)
				for (x = 0; x < this.height; x++)
					person_totals[x] += (totals[y] / total_weighting) 
						* this.get_input(this.row_names[x] + "_" + y);
		}
		
		for (x = 0; x < this.height; x++)
			$(this.row_names[x] + "_t").setValue(this.format_num(person_totals[x]));
		}
	};
