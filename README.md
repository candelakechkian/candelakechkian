## Hi there 👋

**Please note my repos are in progress!**

<table>
  <tr>
    <th>Latest Repositories Released</th>
    <th>Latest Repositories Updated</th>
    <th>Latest Files in <a href="https://github.com/yourusername/YOUR_REPO_NAME">Your Repo</a></th>
  </tr>
  <tr>
    <td>
      <!-- START RELEASES -->
      Loading latest releases...
      <!-- END RELEASES -->
    </td>
    <td>
      <!-- START UPDATED -->
      Loading latest updates...
      <!-- END UPDATED -->
    </td>
    <td>
      <!-- START FILES -->
      Loading latest files...
      <!-- END FILES -->
    </td>
  </tr>
</table>

```python
# about_candela.py

class CandelaKechkian:
    def __init__(self):
        self.name = "Candela Kechkian"
        self.mission = {
            "purpose": "Help all people do things better and do better things",
            "vision": "A world where technology enables us to live more purposefully",
            "priorities": {
                "Advancing Equity": "design with all people in mind, for the benefit of all, and made accessible to all (all people)",
                "Augmenting Human Capabilities": "create more impact (do things better)",
                "Increasing Everyday Efficiencies": "minimize draining tasks and focus on the uniquely human endeavors that bring us joy (do better things)"
            },
            "values": {
                "Efficiency": "",
                "Simplicity": "",
                "Trust": ""
            }
        }
        self.education = [
            {"degree": "B.S. Mechanical Engineering", "school": "Clemson University", "grad_year": 2019},
            {"degree": "B.A. Communication", "school": "Clemson University", "grad_year": 2019},
            {"degree": "MBA, Artificial Intelligence", "school": "Northwestern University", "grad_year": 2026}
        ]
        self.experience = [
            "",
            "",
            ""
        ]
        self.skills = {
            "Technical": ["Python", "", ""],
            "Creative": ["Human-Centered Design", "User-Centered Design", "UX/UI Thinking", "Storytelling & Communication"],
            "Business": ["Business Process Improvement", "Stakeholder Management", "", ""]
        }
        self.interests = ["", "", ""]

    def do_things_better(self):
        return "enhance impact made across all people"

    def do_better_things(self):
        return "enhance purpose across all people"
```

```python
# good_AI_test.py

from about_candela import CandelaKechkian

def benefits_all():
    candela = CandelaKechkian()
    assert "all people" in candela.do_things_better() and "all people" in candela.do_better_things(), "Test failed. AI is not universally beneficial. Do not deploy."
    print("All tests passed. This is good AI.")
```
