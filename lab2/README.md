# Створення додатку бази даних, орієнтованого на взаємодію з СУБД PostgreSQL

## Product
|name|data type|not null|PK|FK|
|--|--|--|--|--|
|id|integer|yes|yes
|name|text|yes|no
|brand|text|no|no
|cost|money|yes|no
|manufacture_date|date|yes|no
|manufacturer|text|yes|no
|category_id|integer|yes|no|Category.id
|order_id|integer|yes|no|Order.id

## Category
|name|data type|not null|PK|FK|
|--|--|--|--|--|
|id|integer|yes|yes
|name|text|yes|no
|type|text|yes|no

## Order
|name|data type|not null|PK|FK|
|--|--|--|--|--|
|id|integer|yes|yes
|transaction_date|date|yes|no
|taxes_sum|money|yes|no
|client_id|integer|yes|no|Client.id

## Client
|name|data type|not null|PK|FK|
|--|--|--|--|--|
|id|integer|yes|yes
|name|text|yes|no
|birthday_date|date|no|no
|email|text|no|no
