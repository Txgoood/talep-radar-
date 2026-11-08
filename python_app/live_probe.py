from scanner import SOURCES, fetch_feed, ScanError
for source in SOURCES:
    try:
        result = fetch_feed(source)
        print(f'{source}: HTTP OK, {result["count"]} feed items, {len(result["candidates"])} candidates', flush=True)
    except ScanError as exc:
        print(f'{source}: unavailable: {str(exc).encode("ascii", "backslashreplace").decode()}', flush=True)
