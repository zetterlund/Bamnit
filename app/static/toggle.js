
        $(document).ready(function() {
            $('.toggle').click(function() {
                var current_status = $('.status').text();
                $.ajax({
                    url: toggle_url,
                    type: "get",
                    data: {status: current_status},
                    success: function(response) {
                        $(".status").html(response);
                    },
                    error: function(xhr) {
                    }
                });
            });
        });
