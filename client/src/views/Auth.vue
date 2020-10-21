<template>
  <div class="auth__block">
    <v-form>
      <v-text-field label="Логин" placeholder="Введите логин"></v-text-field>
      <v-text-field label="Пароль" placeholder="Введите пароль" type="password"></v-text-field>
    </v-form>
  </div>
</template>

<script>
export default {
  name: "Auth"
}
</script>

<style scoped lang="scss">
.auth__block {
  height: auto;
  max-width: 60%;
  margin: 20% auto auto;
}
</style>
