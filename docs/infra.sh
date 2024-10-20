AZREGPASSWORD=""
IMAGE=""
AZREGSERVER=""
AZREGUSER=""
az containerapp env create -n o1vid -g o1vid --location northeurope --enable-workload-profiles
az containerapp sessionpool create \
    --name manim-session-pool8 \
    --resource-group o1vid \
    --environment o1vid \
    --registry-server $AZREGSERVER \
    --registry-username $AZREGUSER \
    --registry-password $AZREGPASSWORD \
    --container-type CustomContainer \
    --location northeurope \
    --cpu 2.0 \
    --memory 4.0Gi \
    --target-port 5000 \
    --cooldown-period 300 \
    --network-status EgressDisabled \
    --max-sessions 10 \
    --ready-sessions 5 \
    --image $IMAGE  
    
    --command "/bin/bash" "-c" "mkdir test; touch test/myfile; tail -f /dev/null"
    \
    --command ["/bin/bash","flask","run","--host=0.0.0.0","--port=5000"]
