# get-images-from-submodules

Github Action to retrieve docker images from the repository mounted at ```/github/workspace```, based on the ```.github/fiware/config.json```.

The action can report the images with their version tag(based on releases in the gitrepos) or without.

## Usage:

```yaml
    - name: Get docker images for submodules
      id: get-images
      uses: FIWARE-Ops/get-images-from-submodules@master
      with:
        includeVersion: true
```

## Output: 

The result is reported as a json list in the output containers. 

Example based on the usage example:

```
    steps.get-images.outputs.containers:
        [
            'orchestracities/quantumleap:0.8.3', 
            'orchestracities/quantumleap:0.8.2', 
            'fiware/orion-ld:1.0.0', 
            'fiware/orion-ld:0.8.0',
            'fiware/iotagent-isoxml:1.0.0'
        ]

``` 