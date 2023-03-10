use futures::executor::block_on;
use sqlx::{migrate::MigrateDatabase, Column, Row, SqlitePool};

pub fn query_db(uri: String, query: String) -> String {
    block_on(async {
        if !sqlx::Sqlite::database_exists(&uri).await.unwrap() {
            sqlx::Sqlite::create_database(&uri).await.unwrap();
        }
        let pool = SqlitePool::connect(&uri).await.unwrap();
        // let query = "DROP TABLE IF EXISTS users;
        // CREATE TABLE users (id INT, name TEXT);
        // INSERT INTO users VALUES(1,'name'),(2,'hey');";
        // sqlx::query(&query).execute(&pool).await.unwrap();
        let rows = sqlx::query(&query).fetch_all(&pool).await;
        let res: String = match rows {
            Ok(rows) => {
                let mut result: String = String::new();
                rows.iter().for_each(|row| {
                    let columns = rows[0].columns();
                    for column in columns {
                        let id: String = row.get_unchecked(column.name());
                        result.push_str(&(id + " "));
                    }
                    result.push_str("\n")
                });
                result
            }
            Err(_) => String::from("Query returned an error"),
        };
        return res;
    })
}
