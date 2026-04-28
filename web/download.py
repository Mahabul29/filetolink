import asyncio
from flask import Response, stream_with_context

def register_download_routes(app, bot, BIN_CHANNEL):

    @app.route('/download/<file_id>')
    def start_download(file_id):
        try:
            bot_loop = asyncio.get_event_loop()
            for loop in asyncio._all_tasks if hasattr(asyncio, '_all_tasks') else []:
                pass
            bot_loop = bot.loop

            msg = asyncio.run_coroutine_threadsafe(
                bot.get_messages(int(BIN_CHANNEL), int(file_id)),
                bot_loop
            ).result(timeout=30)

            if not msg or not msg.document:
                return "File not found.", 404

            doc = msg.document
            file_name = doc.file_name or "download"
            mime_type = doc.mime_type or "application/octet-stream"
            file_size = doc.file_size

            def generate():
                ait = bot.stream_media(msg).__aiter__()
                while True:
                    try:
                        chunk = asyncio.run_coroutine_threadsafe(
                            ait.__anext__(),
                            bot_loop
                        ).result(timeout=60)
                        yield chunk
                    except StopAsyncIteration:
                        break
                    except Exception as e:
                        print(f"Chunk error: {e}")
                        break

            return Response(
                stream_with_context(generate()),
                headers={
                    "Content-Disposition": f'attachment; filename="{file_name}"',
                    "Content-Type": mime_type,
                    "Content-Length": str(file_size),
                }
            )

        except Exception as e:
            print(f"Download error: {e}")
            return f"Error: {str(e)}", 500
