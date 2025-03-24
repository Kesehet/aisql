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

cd ../

python app.py