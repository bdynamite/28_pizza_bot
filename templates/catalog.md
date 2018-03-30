Пицца из нашего меню:

{% for entry in catalog -%}
*{{ entry[0].title }}*
{{ entry[0].description }}
    {%- for choice in entry[1] %}
        {{ choice[1].height }} см, {{ choice[1].weight }} гр (арт {{ choice[1].id }}) - *{{ choice[1].price }} руб.*
    {%- endfor %}

{% endfor %}
