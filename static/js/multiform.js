function cloneFormNodes(nodes, prefix) {
  // Create an array to populate with duplicate set of nodes
  var newNodes = new Array();

  for(var i = 0; i < nodes.length; i++){
    // createElement doesn't work with #test nodes, but since it's just text it can be cloned anyway.
    // All other elements need fresh elements created to modifying the original.
    if(nodes[i].nodeName != "#text") {
      newNodes[i] = document.createElement(nodes[i].nodeName);
    } else {
      newNodes[i] = nodes[i].cloneNode(true)
    }

    // Copy any attributes needed to the new objects, prefixing ids, names and for fields.
    switch(nodes[i].nodeName) {
      case "#text":
        break;
      case "INPUT":
        for(var attrIndex = 0, attrSize = nodes[i].attributes.length; attrIndex < attrSize; attrIndex++){
          newNodes[i].setAttribute(nodes[i].attributes[attrIndex].name, nodes[i].attributes[attrIndex].value);
        }
        newNodes[i].name = prefix + nodes[i].name;
        newNodes[i].id = prefix + nodes[i].id;
        break;
      case "LABEL":
        for(var attrIndex = 0, attrSize = nodes[i].attributes.length; attrIndex < attrSize; attrIndex++){
          newNodes[i].setAttribute(nodes[i].attributes[attrIndex].name, nodes[i].attributes[attrIndex].value);
        }
        newNodes[i].setAttribute('for', prefix + nodes[i].getAttribute('for'));
        break;
      case "OPTION":
        for(var attrIndex = 0, attrSize = nodes[i].attributes.length; attrIndex < attrSize; attrIndex++){
          newNodes[i].setAttribute(nodes[i].attributes[attrIndex].name, nodes[i].attributes[attrIndex].value);
        }
        break;
      case "P":
        for(var attrIndex = 0, attrSize = nodes[i].attributes.length; attrIndex < attrSize; attrIndex++){
          newNodes[i].setAttribute(nodes[i].attributes[attrIndex].name, nodes[i].attributes[attrIndex].value);
        }
        break;
      case "SELECT":
        for(var attrIndex = 0, attrSize = nodes[i].attributes.length; attrIndex < attrSize; attrIndex++){
          newNodes[i].setAttribute(nodes[i].attributes[attrIndex].name, nodes[i].attributes[attrIndex].value);
        }
        newNodes[i].name = prefix + nodes[i].name;
        newNodes[i].id = prefix + nodes[i].id;
        console.log(nodes[i].attributes);
        console.log(newNodes[i]);
        break;
      default:
        console.log("nodeName:", nodes[i].nodeName);
        console.log(nodes[i]);
    }

    // If the current node has children, process them as well.
    if(nodes[i].childNodes.length > 0) {
      var newChildNodes = cloneFormNodes(nodes[i].childNodes, prefix);
      for(var childNodeIndex = 0, size = newChildNodes.length; childNodeIndex < size ; childNodeIndex++){
        newNodes[i].appendChild(newChildNodes[childNodeIndex])
      }
    }
  }
  return newNodes;
}

function createFormItem(templateNodes) {
  if(templateNodes.length > 0) {
    findFormNodes(templateNodes);
  }
}

class Template {
  constructor(baseObject, prefix) {
    // Create a template list of nodes from the nodes in the object and remove the original nodes from the object
    this.container = baseObject;
    this.nodes = Array();
    this.prefix = prefix;
    this.currentIteration = 0;
    this.controlsContainer = document.createElement('div');
    this.addButton = document.createElement('div');
//<div type="button" class="btn btn-success" onclick="addIngredient()">Add ingredient</div><br />
    this.addButton.setAttribute('type', 'button');
    this.addButton.setAttribute('class', 'btn btn-success');
    this.addButton.setAttribute('id', 'multiform-add');
    this.addButton.innerHTML = 'Add';
    console.log(this.addButton);
    //this.addButton.onclick = this.createInstance;
    this.controlsContainer.appendChild(this.addButton);
    console.log("baseObject:", baseObject);
    console.log("childNodes:", baseObject.childNodes);

    for(var i = 0, size = baseObject.childNodes.length; i < size ; i++){
      this.nodes[i] = baseObject.childNodes[0].cloneNode(true);
      baseObject.removeChild(baseObject.childNodes[0]);
    }
    this.container.appendChild(this.controlsContainer);
  }

  createInstance() {
    var prefix = "";
    var instanceContainer = document.createElement('div');

    // Set up the instance prefix which should be "[<prefix>_]<iteration>-".
    if(this.prefix) { prefix = this.prefix + "_"; }
    prefix += this.currentIteration.toString() + "-";

    // Create a set of nodes and populate the new container.
    var nodes = cloneFormNodes(this.nodes, prefix);
    for(var node in nodes) {
      instanceContainer.appendChild(nodes[node]);
    }

    // Increment the iteration counter.
    this.currentIteration++;

    this.container.appendChild(instanceContainer);
  }
}

class MultiformContainer {
  constructor(containerObject) {
    this.container = containerObject;
    this.prefix = prefix;
    this.currentIteration = 0;
    this.controlsContainer = document.createElement('div');
    this.addButton = document.createElement('div');
    this.addButton.setAttribute('type', 'button');
    this.addButton.setAttribute('class', 'btn btn-success');
    this.addButton.setAttribute('id', 'multiform-add');
    this.addButton.innerHTML = 'Add';
    console.log(this.addButton);
    //this.addButton.onclick = this.createInstance;
    this.controlsContainer.appendChild(this.addButton);
    console.log("baseObject:", baseObject);
    console.log("childNodes:", baseObject.childNodes);

    for(var i = 0, size = baseObject.childNodes.length; i < size ; i++){
      this.nodes[i] = baseObject.childNodes[0].cloneNode(true);
      baseObject.removeChild(baseObject.childNodes[0]);
    }
    this.container.appendChild(this.controlsContainer);
  }
}

(function( $ ) {
  /**
   * Build a multi-record form from a jQuery selector.
   * @param {string} prefix - The prefix to set on all field names.
   */
  $.fn.multiForm = function(prefix) {
    // Create a template object from the first object in the jQuery selector.
    var template = new Template(this[0], prefix);

    //var container = new MultiformContainer(this[0]);

    // Create an instance of the template to start the form.
    template.createInstance();

    // Link the click event on the button.....
    $("#multiform-add").click(function() {
      console.log('clicked');
      template.createInstance();
    });

    return this;
  };
}( jQuery ));
