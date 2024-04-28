#include "display_switch.h"

namespace esphome {
namespace haier {

void DisplaySwitch::write_state(bool state) {
  this->publish_state(state);
  this->parent_->set_display_state(state);
}

}  // namespace haier
}  // namespace esphome
