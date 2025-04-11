// stores/teamStore.ts
import { defineStore } from 'pinia';
import { TeamMember } from '../types/TeamMember';

export const useTeamStore = defineStore('team', {
    state: () => ({
        members: [
            {
                name: "Max Muster",
                email: "johndoegmail.com",
                role: "Business Analyst",
                linkedin: "https://www.linkedin.com/in/johndoe",
                phone: "123-456-7890",
                description: "I am a business analyst with 5 years of experience in the IT industry. I have worked on various projects in different domains like finance, healthcare, and e-commerce. I am a quick learner and a team player.",
                profilePic: "src/assets/TeamPhotos/defaultProfilePicture.png"
            },
            {
                name: "John Doe",
                email: "johndoegmail.com",
                role: "Developer",
                linkedin: "https://www.linkedin.com/in/johndoe",
                phone: "123-456-7890",
                description: "I am a full stack developer with 5 years of experience in web development. I have worked with various technologies like React, Angular, Node.js, Express.js, MongoDB, etc. I am passionate about coding and always looking for new challenges. I am a quick learner and a team player. I am open to relocation. ",
                profilePic: "src/assets/TeamPhotos/defaultProfilePicture.png"
            },
            {
                name: "Jane Doe",
                email: "janedoe@gmail.com",
                role: "Developer",
                linkedin: "https://www.linkedin.com/in/johndoe",
                phone: "123-456-7890",
                description: "I am a full stack developer with 5 years of experience in web development. I have worked with various technologies like React, Angular, Node.js, Express.js, MongoDB, etc. I am passionate about coding and always looking for new challenges. I am a quick learner and a team player. I am looking for a full-time position as a full stack developer. I am open to relocation. Feel free to contact me if you have any questions or would like to know more about me. I am looking forward to hearing from you. Thank you.",
                profilePic: "src/assets/TeamPhotos/defaultProfilePicture.png"
            },
            {
                name: "Jane Doe",
                email: "janedoe@gmail.com",
                role: "Developer",
                linkedin: "https://www.linkedin.com/in/johndoe",
                phone: "123-456-7890",
                description: "I am a full stack developer with 5 years of experience in web development. I have worked with various technologies like React, Angular, Node.js, Express.js, MongoDB, etc. I am passionate about coding and always looking for new challenges. I am a quick learner and a team player. I am looking for a full-time position as a full stack developer. I am open to relocation. Feel free to contact me if you have any questions or would like to know more about me. I am looking forward to hearing from you. Thank you.",
                profilePic: "src/assets/TeamPhotos/defaultProfilePicture.png"
            },
        ] as TeamMember[]
    }),
    getters: {
        allMembers: (state) => state.members,
    }
});
