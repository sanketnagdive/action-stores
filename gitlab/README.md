# GitLab API
We use the GitLab REST API for all of our action stores: https://docs.gitlab.com/ee/api/repositories.html#merge-base

# Prompting Tips
1. The GitLab REST API is useful for knowing which parameter inputs are required. Usually, the API that Kubi calls just requires the Group/Project ID. 
2. Kubi can sometimes send unneeded parameters as "", or generate a default value which may lead to errors. When prompting, tell Kubi "Don't send anything other than (needed parameters)."
    - If it repeatedly puts an incorrect parameter, you can try specifying a default value in the Pydantic model using Field()

# Notes on Testing and Common Bugs
1. If ttl.sh is the Docker registry you use, there is often a delay between building using kubiya-cli and ttl.sh receiving the new image (<5 mins). 
2. You may need to restart the pod 3-4 times before it loads all the actions. 
3. Sometimes, the action store will get stuck on pending. If it still hasn't loaded actions after 5-10 minutes, there may be a syntax issue not caught in the building process. 
    1. Delete the action store. 
    2. Check in Kubernetes if the openfaas deployment and pod for your action store has been deleted yet. 
    3. Deploy the action store with your changes. 
4. There appears to be an upper limit of about 125 action stores. Past this limit, the pod will stay stuck on pending. 