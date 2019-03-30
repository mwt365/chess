const modelDropdown = "#select-model";
const colorDropdown = "#select-color";

let retrievedModels = false;
let models = null;

function initButton(id, path) {
  $(`#${id}`).on("click", () => {
    const data = {
      playerColor: $(colorDropdown).val()
    };
    if (retrievedModels) {
      data.backendModel = $(modelDropdown).val();
    } else if (model) {
      data.backendModel = prevModel;
    }
    window.location.href = `/${path}#` + encodeHash(data);
  });
}

const prevData = decodeHash(window.location.hash.substr(1));
const prevColor = prevData.playerColor;
const prevModel = prevData.backendModel;

if (prevColor === "w" || prevColor === "b") {
  $(colorDropdown).val(prevColor);
}

apiRequest(
  {
    command: "list_models"
  },
  response => {
    models = response.models;
    $(modelDropdown).options = [];
    for (const model of models) {
      $(modelDropdown).append(
        new Option(model.displayName, model.internalName)
      );
      if (model.internalName === prevModel) {
        $(modelDropdown).val(prevModel);
      }
    }
    retrievedModels = true;
  }
);

initButton("playBtn", "play");
initButton("aboutBtn", "about");
