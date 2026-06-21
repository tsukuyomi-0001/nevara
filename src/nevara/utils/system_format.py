from datetime import datetime

def get_time_date() -> tuple[str, str]:
    now = datetime.now()
    return now.strftime(f"%d/%m/%Y"), now.strftime(r"%H:%M:%S")

def datetime_formater(summarys: list[str]) -> list[str]:
    docs = []
    for summary in summarys:
        current_date, current_time = get_time_date()
        summary_template = f"[{current_date} - {current_time}] {summary}"
        docs.append(summary_template)
        
    return docs