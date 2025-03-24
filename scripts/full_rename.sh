if [ -z "$VIRTUAL_ENV" ]; then
    if [ -n "$BASH" ]; then
        source myenv/bin/activate
    elif [ -n "$ZSH_VERSION" ]; then
        source myenv/bin/activate.zsh
    else
        echo "Shell not supported"
        exit 1
    fi
fi

cd frontend

npm run build

ollama start &> /dev/null &  # Start ollama in the background without showing logs
OLLAMA_PID=$!  # Capture the process ID





cd ../

python app.py

# Ensure ollama is terminated when the script ends
trap "kill $OLLAMA_PID" EXIT