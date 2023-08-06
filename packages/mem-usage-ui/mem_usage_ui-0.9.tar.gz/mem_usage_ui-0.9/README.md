Description
===========

I'm tired of console measuring of memory usage
```bash
while true; do
ps -C <ProgramName> -o pid=,%mem=,vsz= >> /tmp/mem.log
gnuplot /tmp/show_mem.plt
sleep 1
done &
```

Installation
============

- Python3.7 is a preferable interpreter
- run `pip install mem_usage_ui`

Usage
=====

- Run in shell: `dsmyk$ mem_usage_ui`
- Go to `http://localhost:8080`



![alt text](https://raw.githubusercontent.com/parikls/mem_usage_ui/master/mem_usage_ui.png)


Development
===========

Backend
-------

- Install requirements: `pip install -r requirements.txt`
- Run server: `python -m mem_usage_ui --debug=True`

Frontend
--------

- Go to frontend directory: `cd frontend`
- Install dependencies: `npm install`
- Create (and watch) dev build - `npm run dev`
- Before PR please create a production build `npm run prod`

