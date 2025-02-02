## Hi there 👋

**Please note my repos are in progress!**

<table>
  <tr>
    <th>Latest Releases</th>
    <th>Latest Updates</th>
    <th>Latest TIL</th>
  </tr>
  <tr>
    <td>
      <ul>
        <!-- latest_repos starts -->
* [test](https://github.com/candelakechkian/test)
* [TIL](https://github.com/candelakechkian/TIL)
* [awesome-prompts](https://github.com/candelakechkian/awesome-prompts)
* [the-life-manual](https://github.com/candelakechkian/the-life-manual)
* [awesome-marketing](https://github.com/candelakechkian/awesome-marketing)
<!-- latest_repos ends -->
      </ul>
    </td>
    <td>
      <ul>
        <!-- latest_releases starts -->

<!-- latest_releases ends -->
      </ul>
    </td>
    <td>
      <ul>
        <!-- latest_tils starts -->
* [Geocoding from Python on macOS using pyobjc-framework-CoreLocation](https://github.com/simonw/til/blob/main/python/pyobjc-framework-corelocation.md) - 2025-01-26
* [Downloading every video for a TikTok account](https://github.com/simonw/til/blob/main/tiktok/download-all-videos.md) - 2025-01-19
* [Calculating the size of all LFS files in a repo](https://github.com/simonw/til/blob/main/git/size-of-lfs-files.md) - 2024-12-25
* [Named Entity Resolution with dslim/distilbert-NER](https://github.com/simonw/til/blob/main/llms/bert-ner.md) - 2024-12-24
* [Fixes for datetime UTC warnings in Python](https://github.com/simonw/til/blob/main/python/utc-warning-fix.md) - 2024-12-12
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
