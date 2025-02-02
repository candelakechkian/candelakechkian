## Hi there 👋

**Please note my repos are in progress!**

<table>
  <tr>
    <th>Latest Repos</th>
    <th>Latest Releases</th>
    <th>Latest TIL</th>
  </tr>
  <tr>
    <td>
      <ul>
        <!-- latest_repos starts -->
<li><a href="https://github.com/candelakechkian/TIL">TIL</a> - 2025-02-02</li>
<li><a href="https://github.com/candelakechkian/awesome-prompts">awesome-prompts</a> - 2025-01-21</li>
<li><a href="https://github.com/candelakechkian/the-life-manual">the-life-manual</a> - 2025-01-12</li>
<li><a href="https://github.com/candelakechkian/awesome-marketing">awesome-marketing</a> - 2025-01-12</li>
<li><a href="https://github.com/candelakechkian/badges">badges</a> - 2025-01-08</li>
<!-- latest_repos ends -->
      </ul>
    </td>
    <td>
      <ul>
        <!-- latest_releases starts -->
<li><a href="https://github.com/candelakechkian/TIL">TIL</a> - 2025-02-02</li>
<li><a href="https://github.com/candelakechkian/awesome-prompts">awesome-prompts</a> - 2025-01-21</li>
<li><a href="https://github.com/candelakechkian/awesome-design-resources">awesome-design-resources</a> - 2025-01-18</li>
<li><a href="https://github.com/candelakechkian/awesome-ai-resources">awesome-ai-resources</a> - 2025-01-13</li>
<li><a href="https://github.com/candelakechkian/awesome-marketing">awesome-marketing</a> - 2025-01-12</li>
<!-- latest_releases ends -->
      </ul>
    </td>
    <td>
      <ul>
        <!-- latest_tils starts -->
<li><a href="https://github.com/candelakechkian/TIL/blob/main/README.md">README</a> - 2025-02-02</li>
<!-- latest_tils ends -->
      </ul>
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
            {"degree": "MBA, Artificial Intelligence", "school": "Northwestern University", "grad_year": 2026}
            {"degree": "B.S. Mechanical Engineering", "school": "Clemson University", "grad_year": 2019},
            {"degree": "B.A. Communication", "school": "Clemson University", "grad_year": 2019},
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
