echo "Running Client tests..."
python3 Tests/ClientTests.py
if [ $? -eq 0 ]; then
  echo "All Client tests passed!"
else
  echo "Some Client tests failed."
  exit 1
fi

echo "Done."