#!/bin/bash

REVEAL_CSS=../kirlent_revealjs/static/css/kirlent.css_t
sed "/REVEALJS_EXTRAS/ r revealjs.css" base.css > $REVEAL_CSS
sed -i "/REVEALJS_EXTRAS/d" $REVEAL_CSS
sed -i "/IMPRESSJS_BASICS/d" $REVEAL_CSS

IMPRESS_CSS=../kirlent_impressjs/static/css/kirlent.css_t
sed "/IMPRESSJS_BASICS/ r impressjs.css" base.css > $IMPRESS_CSS
sed -i "/REVEALJS_EXTRAS/d" $IMPRESS_CSS
sed -i "/IMPRESSJS_BASICS/d" $IMPRESS_CSS
