import mysql.connector

class DatabaseManager:
    def __init__(self, host, user, password, database, port=3307):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None

    def connect(self):
        """Veritabanı bağlantısını kurar."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            print("Veritabanına bağlantı başarılı!")
        except mysql.connector.Error as err:
            print(f"Veritabanı bağlantı hatası: {err}")
            self.connection = None

    def close(self):
        """Veritabanı bağlantısını kapatır."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Veritabanı bağlantısı kapatıldı.")

    def execute_query(self, query, params=None):
        """Verilen SQL sorgusunu çalıştırır."""
        if self.connection is None or not self.connection.is_connected():
            raise Exception("Veritabanı bağlantısı mevcut değil.")

        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()
            print("Sorgu başarıyla çalıştırıldı.")
        except mysql.connector.Error as err:
            print(f"Sorgu hatası: {err}")
            raise err

    def fetch_all(self, query, params=None):
        """SQL sorgusundan tüm sonuçları döndürür."""
        if self.connection is None or not self.connection.is_connected():
            raise Exception("Veritabanı bağlantısı mevcut değil.")

        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            return results
        except mysql.connector.Error as err:
            print(f"Veri çekme hatası: {err}")
            raise err

    def fetch_one(self, query, params=None):
        """SQL sorgusundan tek bir sonucu döndürür."""
        if self.connection is None or not self.connection.is_connected():
            raise Exception("Veritabanı bağlantısı mevcut değil.")

        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            result = cursor.fetchone()
            cursor.close()
            return result
        except mysql.connector.Error as err:
            print(f"Veri çekme hatası: {err}")
            raise err

    def delete(self, table, conditions):
        """Belirtilen koşullara göre bir kaydı siler."""
        if not conditions:
            raise ValueError("Koşullar belirtilmeden silme işlemi yapılamaz.")

        where_clause = " AND ".join([f"{key} = %s" for key in conditions.keys()])
        query = f"DELETE FROM {table} WHERE {where_clause}"

        try:
            self.execute_query(query, tuple(conditions.values()))
            print("Kayıt başarıyla silindi.")
        except Exception as err:
            print(f"Silme hatası: {err}")
            raise err

    def insert(self, table, data):
        """Verilen tabloya bir kayıt ekler."""
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        try:
            self.execute_query(query, tuple(data.values()))
            print("Kayıt başarıyla eklendi.")
        except Exception as err:
            print(f"Ekleme hatası: {err}")
            raise err

    def move_to_deleted(self, content_data):
        """Silinen içerikleri deleted_content tablosuna taşır."""
        try:
            self.insert("deleted_content", content_data)
            print("İçerik silinenler tablosuna taşındı.")
        except Exception as err:
            print(f"Silinen tablosuna taşıma hatası: {err}")
            raise err

    def delete_and_archive(self, table, conditions, archive_table="deleted_content"):
        """Bir kaydı hem siler hem de arşiv tablosuna taşır."""
        if not conditions:
            raise ValueError("Koşullar belirtilmeden işlem yapılamaz.")

        # Fetch the record to archive
        where_clause = " AND ".join([f"{key} = %s" for key in conditions.keys()])
        fetch_query = f"SELECT * FROM {table} WHERE {where_clause}"
        record = self.fetch_one(fetch_query, tuple(conditions.values()))

        if record:
            # Insert into archive table
            self.move_to_deleted(record)

            # Delete from original table
            self.delete(table, conditions)
        else:
            print("Belirtilen kayıt bulunamadı.")
