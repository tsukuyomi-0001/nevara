from kokoro import KPipeline
import asyncio

from nevara.modules.util import speed_adjust, play_audio

pipeline = KPipeline(lang_code='a')

audio_queue = asyncio.Queue()
text_queue = asyncio.Queue()

async def generate_all():
    while True:
        text_sample = await text_queue.get()
        if text_sample == None: break
        """
        america: af_bella (best), af_aoede, af_heart (best), af_nicole (huh?), af_nova, af_sky
        british: bf_emma, bf_isabella
        jp: jf_alpha
        china: zf_xiaoni, zf_xiaoxiao
        """
        for _, _, audio in pipeline(text_sample, voice='af_bella', speed=speed_adjust(text_sample)):
            await audio_queue.put(audio)
        
        text_queue.task_done()
        
    await audio_queue.put(None)
       
async def speak_forever():
    while True:
        audio_sample = await audio_queue.get()
        if audio_sample == None: break
        await asyncio.to_thread(play_audio, audio_sample)
        audio_queue.task_done()

async def TTS_engine():
    p = asyncio.create_task(generate_all())
    c = asyncio.create_task(speak_forever())
        
    await p 
    await c