if [ -d "myenv" ]; then
    rm -rf myenv
fi

if ! command -v python &> /dev/null
then
    echo "Python is not installed. Please install it."
    exit
fi
python -m venv myenv
case $SHELL in
  */bash*)
    source myenv/bin/activate
    ;;
  */zsh*)
    source myenv/bin/activate.zsh
    ;;
  *)
    echo "Shell not supported"
    exit 1
esac
pip install -r requirements.txt

mkdir build

cd ../

echo "Installation complete"