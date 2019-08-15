{%- extends 'report_basic.tpl' -%}


{%- block header -%}
<!DOCTYPE html>
<html>
  <head>
    {%- block html_head -%}
    <meta charset="utf-8">
    <link href="report.css" rel="stylesheet">
    {% set nb_title = nb.metadata.get('title', '') or resources['metadata']['name'] %}
    <title>{{nb_title}}</title>
    <meta name="description" content="Report">
    {%- endblock html_head -%}
  </head>
{%- endblock header -%}

{% block body %}
  <body>
  {#    
    <article id="cover">
      <h1>报告样例</h1>
      <address>
        北京市海淀区中关村南路
        天作国际大厦B座2105室
      </address>
      <address>
         xxxyyy@zzz.com
         +10 12345678
      </address>
    </article>
  #}

    {{ super() }}

  </body>
{%- endblock body %}

{% block footer %}
</html>
{% endblock footer %}
