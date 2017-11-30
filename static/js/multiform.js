/**
 * Clone nodes and add a prefix to ids, names, and for attributes on fields and labels.
 * @param {object} nodes - A nodes list of array of nodes to be cloned.
 * @param {string} prefix - The prefix to be added to the ids, names, and for attributes.
 */
function cloneFormNodes(nodes, prefix) {
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

/**
 * Class representing a template instance of the form to be replicated.
 * @class
 */
class Template {
  /**
   * Represents a template instance.
   * @constructor
   * @param {object} baseObject - The DOM object containing the form objects to be templated.
   * @param {string} prefix - The prefix to set on all field names.
   */
  constructor(baseObject, prefix) {
    this.nodes = Array();
    this.prefix = prefix;
    this.currentIteration = 0;

    // Create a template list of nodes from the nodes in the baseObject and remove the original nodes.
    for(var nodeIndex = 0, nodeCount = baseObject.childNodes.length; nodeIndex < nodeCount; nodeIndex++){
      this.nodes[nodeIndex] = baseObject.childNodes[0].cloneNode(true);
      baseObject.removeChild(baseObject.childNodes[0]);
    }
  }

  /**
   * Creates a new instance from the template.
   * @return {object} A div element containing a clone of the nodes in this template.
   */
  createInstance() {
    var prefix = "";
    var nodes;
    var instanceContainer = document.createElement('div');

    // Set up the instance prefix as "[<prefix>_]<iteration>-".
    if(this.prefix){
      prefix = this.prefix + "_";
    }
    prefix += this.currentIteration.toString() + "-";

    // Create a set of nodes and populate the new container.
    nodes = cloneFormNodes(this.nodes, prefix);
    for(var node in nodes) {
      instanceContainer.appendChild(nodes[node]);
    }

    // Increment the iteration counter.
    this.currentIteration++;

    return instanceContainer;
  }
}

/**
 * Class representing the container for the multiform instances and controls.
 * @class
 */
class MultiformContainer {
  /**
   * Represents a container instance.
   * @constructor
   * @param {object} containerObject - The DOM object containing multiform.
   */
  constructor(containerObject) {
    this.container = containerObject;
    this.controlsContainer = document.createElement('div');
    this.addButton = document.createElement('div');

    this.addButton.innerHTML = 'Add';
    this.addButton.setAttribute('type', 'button');
    this.addButton.setAttribute('class', 'btn btn-success');
    this.addButton.setAttribute('id', 'multiform-add');
    this.controlsContainer.appendChild(this.addButton);
    this.container.appendChild(this.controlsContainer);
  }

  /**
   * Append a child to the container.  This is simply created to prevent container.container.appendChild()
   * @param {object} child - The DOM object to append to the container
   */
  appendChild(child) {
    this.container.appendChild(child);
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

    var container = new MultiformContainer(this[0]);

    // Create an instance of the template to start the form.
    container.appendChild(template.createInstance());

    // When the add button is clicked create an instance of the template and append it to the container.
    $("#multiform-add").click(function() {
      container.appendChild(template.createInstance());
    });

    return this;
  };
}( jQuery ));
