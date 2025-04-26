LOG_FILE = 'log.txt'

f = open(LOG_FILE, 'a+', encoding='utf-8')

def safe_str(val):
    return str(val) if val is not None and val != "" else ""

def log(lvl, msg, *args, **kwargs):
    msg = safe_str(msg)
    args = tuple(safe_str(a) for a in args)
    kwargs = {k: safe_str(v) for k, v in kwargs.items()}
    record_text = f'[{lvl}]: {msg} {args} {kwargs}'
    print(record_text)
    f.write(record_text + '\n')

def info(msg, *args, **kwargs):
    log('Info', msg, *args, **kwargs)

def warning(msg, *args, **kwargs):
    log('Warning', msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    log('Error', msg, *args, **kwargs)

def workInfo(msg):
    msg = safe_str(msg)
    record_text = f'[artworkInfo]: {msg}'
    print(msg)
    f.write(record_text + '\n')