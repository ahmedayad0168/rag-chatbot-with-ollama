import torch

from transformers import AutoTokenizer
from transformers import AutoModelForSeq2SeqLM

from config import MODEL_PATH
from config import MAX_SQL_ROWS

# from sql.schema import SCHEMA    
from sql.validator import clean_sql
from sql.validator import validate_sql
from sql.db import connect_db


class SQLAgent:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.tokenizer = AutoTokenizer.from_pretrained(str(MODEL_PATH))
        self.model = AutoModelForSeq2SeqLM.from_pretrained(str(MODEL_PATH)).to(self.device)
        self.model.eval()

    def generate_sql(self, question):
        input_text = f"translate English to SQL: {question}"

        inputs = self.tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512).to(self.device)
        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_length=256, num_beams=4, early_stopping=True)

        sql = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return clean_sql(sql)

    def execute_sql(self, sql):
        conn = connect_db()
        try:            
            cursor = conn.cursor()
            cursor.execute(sql)

            if cursor.description:
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchmany(MAX_SQL_ROWS)

                result = [" | ".join(columns), "-" * 50]
                result.extend(" | ".join(str(v) for v in row) for row in rows)
                return "\n".join(result)

            conn.commit()
        finally:
            conn.close()   

    def ask(self, question):
        sql = self.generate_sql(question)
        valid, message = validate_sql(sql)

        if not valid:
            return {"answer": f"Blocked query: {message}", "sql": sql}

        try:
            result = self.execute_sql(sql)
            return {"answer": result or "Query executed successfully.", "sql": sql}

        except Exception as e:
            return {"answer": f"Error executing query: {e}", "sql": sql} 