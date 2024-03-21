памятка основных команд для работы через Dev Tools с Elasticsearch:

1. Создание индекса:

```
PUT /my_index
```

2. Удаление индекса:

```
DELETE /my_index
```

3. Добавление документа в индекс:

```
POST /my_index/_doc
{
  "field1": "value1",
  "field2": "value2"
}
```

4. Получение документа по ID:

```
GET /my_index/_doc/my_id
```

5. Обновление документа:

```
POST /my_index/_doc/my_id/_update
{
  "doc": {
    "field1": "new_value1"
  }
}
```

6. Удаление документа:

```
DELETE /my_index/_doc/my_id
```

7. Поиск документов:

```
GET /my_index/_search
{
  "query": {
    "match": {
      "field1": "value1"
    }
  }
}
```

8. Сортировка результатов поиска:

```
GET /my_index/_search
{
  "query": {
    "match_all": {}
  },
  "sort": [
    { "field1": "asc" }
  ]
}
```

9. Агрегация результатов поиска:

```
GET /my_index/_search
{
  "aggs": {
    "my_agg": {
      "terms": {
        "field": "field1"
      }
    }
  }
}
```

10. Получение информации о состоянии кластера:

```
GET /_cluster/health
```

11. Получение информации о состоянии узлов кластера:

```
GET /_cat/nodes?v
```

12. Получение информации о состоянии индексов:

```
GET /_cat/indices?v
```
