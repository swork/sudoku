# sudoku
Sudoku solver in Python. Includes WSGI adapter, but seriously wants an OCR front-end.
```
$ cat << EOF > puzzle.json
[
  [ 0, 0, 9, 0, 7, 0, 0, 8, 4 ],
  [ 0, 7, 6, 8, 0, 9 ],
  [ 0, 0, 0, 0, 0, 3, 0, 0, 2 ],
  [ 0, 1, 0, 0, 3 ],
  [ 0, 2, 0, 4 ],
  [ 0, 0, 0, 9, 2, 0, 0, 6 ],
  [ 0, 0, 7, 6, 5, 4, 0, 3 ],
  [ 0, 5, 0, 0, 0, 1 ],
  [ 0, 0, 0, 0, 0, 2, 0, 9 ]
]
EOF
$ python3 -m renlabs.sudoku.cli --json @puzzle.json
[[1,3,9,2,7,5,6,8,4],[2,7,6,8,4,9,3,1,5],[5,8,4,1,6,3,9,7,2],[6,1,8,5,3,7,4,2,9],[9,2,3,4,1,6,7,5,8],[7,4,5,9,2,8,1,6,3],[8,9,7,6,5,4,2,3,1],[3,5,2,7,9,1,8,4,6],[4,6,1,3,8,2,5,9,7]]
```
A WSGI application object `application` is in `import renlabs.sudoku.api`.
