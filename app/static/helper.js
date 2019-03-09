
        var toggle_url = "{{ url_for('main.toggled_status') }}";

        var c1_labels = {{ d['g1']['labels']|tojson }};
        var c1_legend = "{{ d['g1']['legend'] }}";
        var c1_values = {{ d['g1']['values']|tojson }};

        var c2_labels = {{ d['g2']['labels']|tojson }};
        var c2_legend = "{{ d['g2']['legend'] }}";
        var c2_values = {{ d['g2']['values']|tojson }};
