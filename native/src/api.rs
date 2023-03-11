use futures::executor::block_on;
use sqlx::{migrate::MigrateDatabase, sqlite::SqlitePoolOptions, Column, Row};

pub fn query_db(uri: String, query: String) -> String {
    block_on(async {
        if !sqlx::Sqlite::database_exists(&uri).await.unwrap() {
            sqlx::Sqlite::create_database(&uri).await.unwrap();
        }
        let pool = SqlitePoolOptions::new()
            .max_connections(1)
            .connect(&uri)
            .await
            .unwrap();
        // let init = "DROP TABLE IF EXISTS users;
        // CREATE TABLE IF NOT EXISTS users (id INT, name TEXT);
        // INSERT INTO users VALUES(1,'name'),(2,'hey');";
        // sqlx::query(&init).execute(&pool).await.unwrap();
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
            Err(err) => {
                let mut result: String = String::from("Query returned an error: ");
                let msg: String = format!("{}", err);
                result.push_str(&msg);
                result
            }
        };
        return res;
    })
}
