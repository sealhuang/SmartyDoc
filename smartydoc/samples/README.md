Step 1: Download fonts from https://pan.baidu.com/s/1oOJQawsrWQAmHioCu9EGow (extract code: b6vk), and put the ttf files into fonts directory.

Step 2: run command `jupyter-nbconvert --execute --to html --template=../templates/report_sample.tpl report_sample.ipynb --output test.html`

Step 3: run `trans2std --in test.html --toc_level 1 --add_heading_number --out_file std.html`

Step 4: run `weasyprint std.html report_sample.pdf`

