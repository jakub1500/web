if [ -n "$VIRTUAL_ENV" ]; then
    echo "Running in a virtual environment: $VIRTUAL_ENV"
else
    echo "Script must be executed in virtual environment"
    exit 1
fi

pip install -r requirements.txt
python main.py