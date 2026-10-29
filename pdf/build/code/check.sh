while true; do
  echo "Request at $(date):"

  curl -s -X POST http://myapp.local:30080/auth \
       -H "Content-Type: application/json" \
       -d '{"query":"{ healthz }"}'
  echo -e "\n---------------------------\n"

  curl -s -X POST http://myapp.local:30080/products \
       -H "Content-Type: application/json" \
       -d '{"query":"{ healthz }"}'
  echo -e "\n---------------------------\n"

  curl -s -X POST http://myapp.local:30080/orders \
       -H "Content-Type: application/json" \
       -d '{"query":"{ healthz }"}'
  echo -e "\n---------------------------\n"

  sleep 5
done
