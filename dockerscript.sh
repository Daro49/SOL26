#!/bin/bash

# --- KONFIGURÁCIA ---
LOGIN="xdaranm00"
IMAGE_TAG="${LOGIN}"
INT_DIR="./int"
TESTER_DIR="./tests/testy"


case "$1" in
    check)
        echo "--- Building stage: CHECK ---"
        sudo docker build --target check --tag "${IMAGE_TAG}:check" .
        
        echo "--- Running interactive CHECK container ---"
        echo "Tip: Run './ruff check' or './eslint --format json src/' inside."
        sudo docker run --rm -it \
            -v "${INT_DIR}:/src/int/" \
            -v "${TESTER_DIR}:/src/tester/" \
            "${IMAGE_TAG}:check"
        ;;

    build)
        echo "--- Building stage: BUILD (Capturing logs) ---"
        sudo docker build --target build --progress plain . 2>"${LOGIN}_build.log"
        echo "Build finished. Check '${LOGIN}_build.log' for compiler output."
        ;;

    runtime)
        echo "--- Building stage: RUNTIME ---"
        sudo docker build --target runtime --tag "${IMAGE_TAG}:runtime" .
        
        echo "--- Running RUNTIME with examples ---"
        sudo docker run --rm -v "$(pwd)/examples:/tmp/" "${IMAGE_TAG}:runtime" -s /tmp/example2.out
        ;;

    test)
        echo "--- Building stage: TEST ---"
        sudo docker build --target test --tag "${IMAGE_TAG}:test" .
        
        echo "--- Running tests per folder ---"
        if [ -d "./tests" ]; then
            # Prejdeme všetky podpriecinky v ./tests
            for dir in ./tests/*/; do
                # Získame názov priečinka (napr. claude, random, zadani)
                folder_name=$(basename "$dir")
                
                # Preskočíme, ak to nie je priečinok (pre istotu)
                [ -d "$dir" ] || continue

                echo "=> Testing folder: $folder_name"

                # Spustíme docker pre konkrétny priečinok
                # Výstup (JSON) presmerujeme do report_<meno>.json
                # V kontajneri mierime na /opt/tests/<meno>
                sudo docker run --rm \
                    -v "$(pwd)/tests:/opt/tests" \
                    "${IMAGE_TAG}:test" -r "/opt/tests/$folder_name" \
                    > "report_${folder_name}.json"

                echo "   Done. Report saved to report_${folder_name}.json"
            done
        else
            echo "Error: Directory './tests' not found."
            exit 1
        fi
        ;;

    *)
        echo "Usage: $0 {check|build|runtime|test|clean}"
        exit 1
        ;;
esac