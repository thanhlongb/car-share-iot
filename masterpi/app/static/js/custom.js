(function(){
    $(window).scroll(function () {
        var top = $(document).scrollTop();
        if(top > 50)
          $('#home > .navbar').removeClass('navbar-transparent');
        else
          $('#home > .navbar').addClass('navbar-transparent');
    });
  
    $("a[href='#']").click(function(e) {
      e.preventDefault();
    });
  
    $('.bs-component [data-toggle="popover"]').popover();
    $('.bs-component [data-toggle="tooltip"]').tooltip();
    
    function cleanSource(html) {
      html = html.replace(/×/g, "&times;")
                 .replace(/«/g, "&laquo;")
                 .replace(/»/g, "&raquo;")
                 .replace(/←/g, "&larr;")
                 .replace(/→/g, "&rarr;");
  
      var lines = html.split(/\n/);
  
      lines.shift();
      lines.splice(-1, 1);
  
      var indentSize = lines[0].length - lines[0].trim().length,
          re = new RegExp(" {" + indentSize + "}");
  
      lines = lines.map(function(line){
        if (line.match(re)) {
          line = line.substring(indentSize);
        }
  
        return line;
      });
  
      lines = lines.join("\n");
  
      return lines;
    }
  
  })();
  