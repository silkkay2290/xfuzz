#not completed
import aiohttp
import asyncio
import sys
async def fuzz(args):
    """Fuzz a target URL with the command-line arguments specified by ``args``."""
    queue = asyncio.Queue()
    urls = []
    tasks = []
    print(f"args = {args}")
    # TODO: your code here!
    if "FUZZ" in args.url:
        if(args.wordlist == "-"):
            for line in sys.stdin:
                if(len(args.extensions) == 0):
                    new_url = args.url.replace("FUZZ", line)
                    urls.append(new_url)
                else:
                    for i in range(len(args.extensions)):
                        new_url = args.url.replace("FUZZ", line)
                        new_url += args.extensions[i]
                        urls.append(new_url)
        else:
            f = open(args.wordlist, "r")
            for x in f:
                if(len(args.extensions) == 0):
                    new_url = args.url.replace("FUZZ", x)
                    urls.append(new_url)
                else:
                    for i in range(len(args.extensions)):
                        new_url = args.url.replace("FUZZ", x)
                        new_url += args.extensions[i]
                        urls.append(new_url)
    else:
        for i in range(len(args.headers)):
            if "FUZZ" in args.headers[i]:
                if(args.wordlist == "-"):
                    for line in sys.stdin:
                        if(len(args.extensions) == 0):
                            new_url = args.headers[i].replace("FUZZ",line)
                            stripped1 = new_url.strip() 
                            stripped = stripped1.replace(" ", "")
                            # print(stripped)
                            temp = stripped.split(":")
                            urls.append((temp[0],temp[1]))
                        else:
                            for i in range(len(args.extensions)):
                                new_url = args.headers[i].replace("FUZZ",line)
                                new_url += args.extensions[i]
                                urls.append(new_url)
                else:
                    f = open(args.wordlist, "r")
                    for x in f:
                        if(len(args.extensions) == 0):
                            new_url = args.headers[i].replace("FUZZ",x)
                            stripped1 = new_url.strip() 
                            stripped = stripped1.replace(" ", "")
                            # print(stripped)
                            temp = stripped.split(":")
                            urls.append((temp[0],temp[1]))
                        else:
                            for i in range(len(args.extensions)):
                                new_url = args.headers[i].replace("FUZZ",x)
                                new_url += args.extensions[i]
                                urls.append(new_url)
                # args.headers[i].replace("FUZZ",x)
    # Create a scheduler task to queue up jobs
    s = asyncio.create_task(scheduler(queue, urls))
    tasks.append(s)

    # Create workers to consume jobs
    for _ in range(40):
        w = asyncio.create_task(start_worker(queue,args))
        tasks.append(w)

    # Wait for the scheduler and the workers to finish
    await asyncio.gather(*tasks)   
    
async def scheduler(queue, jobs):
  # Put jobs onto the queue so that workers can execute them
  for job in jobs:
    await queue.put(job)

  # Put None onto the queue once for each worker so that they know
  # there isn't any more work to do
  for _ in range(len(jobs)):
    await queue.put(None)


async def start_worker(queue, args):
  while True:
    # Get some new work off the queue
    job = await queue.get()

    try:
      # If the job is `None`, there's no more work to do, so the
      # worker can exit
      if job is None:
        break

      async with aiohttp.ClientSession() as session:
        if(len(args.headers) == 0 ):
            async with session.get(job) as resp:
                for i in range(len(args.match_codes)):
                    if(args.match_codes[i]==resp.status):
                        print(f"{job} - Status {resp.status}")
        else:
            dict = {
                job[0]: job[1]
            }
            
            async with session.get(args.url, headers=dict) as resp:
                for i in range(len(args.match_codes)):
                    if(args.match_codes[i]==resp.status):
                        print(f"{job} - Status {resp.status}")

    finally:
      # Mark the job as being completed
      queue.task_done()
        
#     # ex: print the arguments that were passed in to this function
#     print(f"args = {args}")
#     # ex: make an HTTP request to the input URL
#     async with aiohttp.ClientSession() as session:
#         for u in urls:
#             task = asyncio.create_task(session.request("GET", u))
#             tasks.append(task)
#         responses = await asyncio.gather(*tasks)
#         for x in range(len(responses)):
#             print (responses[x])
#             # async with session.get(y) as resp:
#             #         if(args.match_codes[0] == resp.status):
#             #             print(f"{y} - Status {resp.status}")
# if __name__ == "__fuzz__":
#   asyncio.run(fuzz())