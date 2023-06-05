const selectList = [
  "character", "text", "integer", "float", "boolean", "date"
]
const formList = document.querySelector("#form-list")
const addButton = document.querySelector("#add_field")
let fieldNumber = 0

const showMoreFields = () => {
  fieldNumber ++
  const inputGroup = document.createElement("div")
  inputGroup.className = "input-group my-3"
  formList.appendChild(inputGroup)

  const fieldNameInput = document.createElement("input")
  fieldNameInput.type = "text"
  fieldNameInput.name = `name_field_${fieldNumber}`
  fieldNameInput.placeholder = `field_${fieldNumber} name...`
  fieldNameInput.className = "form-control form-control-lg"
  inputGroup.appendChild(fieldNameInput)

  const fieldTypeInput = document.createElement("select")
  fieldTypeInput.name = `type_field_${fieldNumber}`
  fieldTypeInput.className = "form-control form-control-lg"
  for (const val of selectList) {
    const option = document.createElement("option")
    option.value = val
    option.text = val
    fieldTypeInput.appendChild(option)
  }
  inputGroup.appendChild(fieldTypeInput)
}


addButton.addEventListener("click", showMoreFields)