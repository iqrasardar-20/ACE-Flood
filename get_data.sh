#!/usr/bin/env bash
# Downloads the CAMELS-US 4-basin subset (2000-2002) used in the paper from the NeuralHydrology repository.
set -e
cd "$(dirname "$0")"
mkdir -p data && cd data
git clone --depth 1 --filter=blob:none --sparse https://github.com/neuralhydrology/neuralhydrology.git nh_tmp
cd nh_tmp && git sparse-checkout set test/test_data/camels_us && cd ..
rm -rf camels_us && cp -r nh_tmp/test/test_data/camels_us camels_us && rm -rf nh_tmp
echo "Data ready in data/camels_us"
