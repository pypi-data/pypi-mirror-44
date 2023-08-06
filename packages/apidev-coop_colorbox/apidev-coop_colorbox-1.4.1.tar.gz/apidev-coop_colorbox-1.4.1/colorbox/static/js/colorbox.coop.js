$(function() {
    var reloadRegex = /reload: (.*)$/;

    /* Colorbox resize function */
    var resizeTimer;
    function resizeColorBox() {
        if (resizeTimer) {
          clearTimeout(resizeTimer);
        }
        resizeTimer = setTimeout(function() {
            if ($('#cboxOverlay').is(':visible')) {
                $.colorbox.resize();
            }
        }, 300);
    }
    // Resize Colorbox when resizing window or changing mobile device orientation
    $(window).resize(resizeColorBox);
    $(document).on("orientationchange", resizeColorBox);

    var _process_form_result = function(html, options) {

        if (html.match(/^<script>.*<\/script>$/)) {
            $('body').append(html);
        } else if (html.match(reloadRegex)) {
            var url = html.match(reloadRegex)[1];
            $.colorbox({
                maxWidth: '90%',
                top: 0,
                trapFocus: false,
                href : url,
                title : '...',
                onComplete : function(){
                    _colorboxify_form(options);
                }
            });
        }
        else if (html === 'close_popup') {
            $.colorbox.close();
        } else if (options && options.hasOwnProperty(html)) {
            options[html].call(this);
        } else {
            $.colorbox({
                maxWidth: '90%',
                top: 0,
                trapFocus: false,
                html:html,
                title : '...',
                onComplete : _colorboxify_form
            });
        }
    };
    
    var _colorboxify_form = function(options) {
        $("form.colorbox-form").ajaxForm({
            success: function(html) {
                _process_form_result(html, options);
            }
        });    
    };
    
    $.fn.colorboxify = function(options) {
        $(document).on('click', "a.colorbox-form", function () {
            $.colorbox({
                maxWidth: '90%',
                top: 0,
                trapFocus: false,
                href : $(this).attr('href'),
                title : '...',
                onComplete : function(){
                    _colorboxify_form(options);
                }
            });
            return false;
        });
    };

     $.fn.showColorbox = function(href, options) {
          $.colorbox({
              maxWidth: '90%',
              top: 0,
              trapFocus: false,
              href: href,
              title: '...',
              onComplete: function () {
                _colorboxify_form(options);
              }
          });
     };
    
    $.fn.colorboxSubmit = function(options) {
        $(this).ajaxSubmit({
            url: options.href,
            resetForm: true,
            success: function(html) {
                $.colorbox({
                    maxWidth:'90%',
                    top: 100,
                    html:html,
                    title : '...',
                    onComplete : function(){
                        _colorboxify_form(options);
                    }
                });
            }
        });
    };
});