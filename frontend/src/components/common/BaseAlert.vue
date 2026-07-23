<script setup>
defineProps({
  variant: { type: String, default: 'error' }
})

const variantes = {
  error: 'bg-red-100 text-red-800 border-red-300',
  success: 'bg-green-100 text-green-800 border-green-300',
  warning: 'bg-yellow-100 text-yellow-800 border-yellow-300'
}
</script>

<template>
  <div class="border rounded-md px-4 py-3 text-sm" :class="variantes[variant]">
    <slot />
  </div>
</template>
