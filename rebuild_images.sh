#!/bin/bash
# Rebuild every site image from its ORIGINAL camera photo using real background
# replacement (rembg cut-out + studio plate). No generative model touches the product,
# so wiring, wrap colour and connectors are exactly as photographed.
set -u
PY=".venv-bg/bin/python"
SRC="photos_jpg"
OUT="images"
run () { # out  source  [extra args]
  o="$OUT/$1"; shift; s="$SRC/$1"; shift
  if ! $PY replace_bg.py "$s" "$o" "$@" 2>>rebuild_errors.log; then
    echo "FAILED $o  <- $s"
  fi
}

# --- home page ---
run hero-21700.jpg  "IMG_4055.jpg"
run hero-hd.jpg     "IMG_4006.jpg"
run hero-ev.jpg     "IMG_4019 (1).jpg"
run type-21700.jpg  "IMG_4054.jpg"
run type-hd.jpg     "IMG_4006.jpg"
run type-ev.jpg     "IMG_4019 (1).jpg"
run about.jpg       "IMG_4058.jpg"
run g1.jpg          "IMG_4008.jpg"
run g2.jpg          "IMG_4017.jpg"
run g3.jpg          "IMG_4009.jpg"
run g4.jpg          "IMG_4052.jpg"
run g5.jpg          "IMG_4013.jpg"
run g6.jpg          "IMG_4037 (3).jpg"
run b1.jpg          "IMG_4053.jpg"
run b2.jpg          "IMG_4005 (1).jpg"
run b3.jpg          "IMG_4029.jpg"
run b4.jpg          "IMG_4022.jpg"
run b5.jpg          "IMG_4038 (2).jpg"
run b6.jpg          "IMG_4020.jpg"

# --- wide banners: 16:9, pack in the right third ---
run hero-wide.jpg   "IMG_4055.jpg"    --ratio 1.7778 --anchor right --pad 0.10
run cta-wide.jpg    "IMG_4034 (1).jpg" --ratio 1.7778 --anchor right --pad 0.10

# --- product pages ---
run p21-1.jpg "IMG_4033 (1).jpg";  run p21-2.jpg "IMG_4035 (2).jpg"
run p21-3.jpg "IMG_4036 (2).jpg";  run p21-5.jpg "IMG_4056.jpg"
run p21-6.jpg "IMG_4057.jpg"
run phd-1.jpg "IMG_4007 (1).jpg";  run phd-2.jpg "IMG_4005 (1).jpg"
run phd-3.jpg "IMG_4006.jpg";      run phd-4.jpg "IMG_4052.jpg"
run pev-1.jpg "IMG_4028 (2).jpg";      run pev-2.jpg "IMG_4024 (1).jpg"
run pev-3.jpg "IMG_4031 (2).jpg"
echo DONE
