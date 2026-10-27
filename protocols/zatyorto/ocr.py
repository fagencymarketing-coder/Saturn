import sys, json, subprocess, csv, io, os
def words(img):
    out = subprocess.run(['tesseract', img, 'stdout', '-l', 'rus', '--psm', '6', 'tsv'],
                         capture_output=True, text=True).stdout
    rows=[]
    for r in csv.DictReader(io.StringIO(out), delimiter='\t', quoting=csv.QUOTE_NONE):
        try:
            if r['text'] and r['text'].strip() and float(r["conf"])>0:
                rows.append({'t':r['text'].strip(),'x':int(r['left']),'y':int(r['top']),
                             'w':int(r['width']),'h':int(r['height']),
                             'line':(int(r['block_num']),int(r['par_num']),int(r['line_num']))})
        except Exception: pass
    return rows
if __name__=='__main__':
    f=sys.argv[1]
    ws=words(f)
    # print line by line with coords
    cur=None
    for w in ws:
        if w['line']!=cur:
            cur=w['line']; print()
            print('Y%4d |'%w['y'], end=' ')
        print('%s[%d-%d]'%(w['t'],w['x'],w['x']+w['w']), end=' ')
    print()
