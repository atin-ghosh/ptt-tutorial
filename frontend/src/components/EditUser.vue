<template>
  <div class = "container-edit">
      <form @submit="onSubmit" class="add-form">
          <img src="../atin_photo2.jpg" class="head-img" alt="hello" width="150" height="150">
          <div class="form-control-3">
              <img src="../company.png" class="icon-img" alt="Company">
              <input type="text" style="width: 160px," v-model="company" name="company" />
          </div>
          <div class="form-control-3">
              <img src="../location.png" class="icon-img" alt="Location">
              <input type="text" style="width: 160px," v-model="location" name="location" />
          </div>
          <div class="form-control-3">
              <img src="../mail.png" class="icon-img" alt="Email">
              <input type="text" style="width: 160px," v-model="email" name="email" />
          </div>
          <div class="form-control-3">
              <img src="../phone.png" class="icon-img" alt="Tel">
              <input type="text" style="width: 160px," v-model="telephone" name="telephone" />
          </div>
          <input type="submit" value="Save Edits" class="editButtonSave" />
      </form>
  </div>
</template>

<script>
export default {
  name: 'EditUser',
  data() {
    return {
        username: '',
        company: '',
        location: '',
        email: '',
        telephone: '',
    }
  },
  props:{
    parentData: Object,
  },
  emits: ['edit-user'],
  methods: {
    onSubmit(e) {
        e.preventDefault()
        if (!this.company || !this.location || !this.email || !this.telephone) {
            alert('Please input edits')
            return
        }
        const editDetails = {
            company: this.company,
            location: this.location,
            email: this.email,
            telephone: this.telephone
        }
        this.$emit('edit-user', editDetails)
        this.company = ''
        this.location = ''
        this.email = ''
        this.telephone = ''
    },
  },
  created() {
    this.username = localStorage.getItem("sessionUsername")
    this.company = this.parentData.company
    this.location = this.parentData.location
    this.email = this.parentData.email
    this.telephone = this.parentData.telephone
  }
}
</script>

<style scoped>

.container-edit {
  width: 375px;
  text-align: left;
  background: rgb(255, 255, 255);
  margin: 30px auto;
  overflow: auto;
  min-height: 350px;
  border: 1px solid steelblue;
  text-align: center;
  padding: 50px;
  border-radius: 5px;
}

.head-img {
  border-radius: 50%;
  margin-bottom: 30px;
  width: 250px;
  height: 250px;
}

.form-control-3 {
  display: flex;
  justify-content: space-between;
}

.add-form {
  display: inline-block;
}

.editButtonSave {
    display: inline-block;
    background: rgb(31, 190, 31);
    color: black;
    width:250px;
    border: none;
    margin: 5px;
    border-radius: 5px;
    cursor: pointer;
    border: 1px solid steelblue;
    text-decoration: none;
    font-size: 15px;
    font-family: inherit;
    margin-top: 15px;
}

label {
    float: left;
    width: 113px;
}

</style>