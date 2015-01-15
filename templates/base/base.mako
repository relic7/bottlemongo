<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>${self.attr.title}</title>
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta name="description" content="{% block meta_description %}{% endblock %}">
    <meta name="author" content="{% block meta_author %}{% endblock %}">

  <!-- Mobile viewport optimized: h5bp.com/viewport -->
  <meta name="viewport" content="width=device-width">
    <link type="text/css" href="/static/css/main.css" rel="stylesheet">
    <script type="text/javascript">
    function toggle(id) {
        var el = document.getElementById(id);
        el.style.display = (el.style.display != 'none' ? 'none' : '' );
    }
    </script>
</head>
<body>
    <a href="/" alt="refresh_home"><h1>${self.attr.title}</h1></a>
    ${self.body()}
</body>
</html>
