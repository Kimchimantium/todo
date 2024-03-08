# Project Title

A brief description of what this project does and who it's for.

## Features

This project includes several interactive features to enhance the user interface and user experience:

### Collapse Animation for Tables

- **Caret Rotation**: Utilizes `anime.js` to animate caret icons for a smooth visual indication when table sections are expanded or collapsed.
    - The caret icon (`fa-caret-up`) rotates 180 degrees when its associated collapsible section is expanded, indicating that the section can be collapsed by clicking the icon again.
    - When the section is collapsed, the icon rotates back, indicating the section can be expanded.

### Dynamic Countdown Timers

- Implements JavaScript countdown timers for tasks with a specific deadline.
    - Each task has a timer counting down to its deadline, displayed in days, hours, minutes, and seconds.
    - When the timer reaches the deadline, it displays "EXPIRED" or "OUTDATED," depending on the context.

### Color Coding for Timers

- Timers are dynamically color-coded based on the time remaining to the deadline.
    - Less than 1 hour: Red
    - Less than 3 hours but more than 1 hour: Orange
    - More than 3 hours but less than a day: Green
    - Outdated tasks are marked in grey.

## Implementation

### JavaScript Event Listeners

- The functionalities are implemented using JavaScript event listeners that trigger on specific actions (e.g., when a collapsible section is shown or hidden).
- The countdown logic calculates the time remaining to the deadline for each task and updates the display in real-time.

### Dependencies

- `anime.js` for animations.
- Bootstrap for styling and collapsible components.

## How to Use

To see the features in action, simply load the `index.html` page in a browser. Interact with the collapsible sections and observe the countdown timers for tasks with deadlines.

## Contributing

Contributions to enhance or extend the functionalities are welcome. Please follow the standard pull request process.

## License

Specify the project license here.
